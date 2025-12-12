#
#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

import logging
import math
import random
import sys
import traceback
from datetime import datetime
from enum import IntEnum
from enum import unique
import torch

import numpy as np
import pandas as pd
from dateutil.parser import parse as DateUtilParse
from pytimeparse import parse as DateIntervalParse  # pip install pytimeparse

logger = logging.getLogger(__name__)


def isnan_or_null_no_crash(x):
    try:
        return math.isnan(x)
    except:
        if x is None:
            return True
    if x == "nan" or x == "NaN":
        return True
    return False


@unique
class ColumnType(IntEnum):
    SCALAR = 0
    SET = 1
    TIMESTAMP = 2
    LIST_OF_SETS = 3
    FREE_STRING = 4
    EMAIL = 5
    TIME_INTERVAL = 6
    DOMAIN = 7
    VECTOR = 8
    JSON = 9


from babel.numbers import parse_decimal, parse_number
from sklearn.preprocessing import OneHotEncoder  # LabelBinarizer, LabelEncoder,


def _isNumber(s):
    """
    This function is a big part of Featrix IP. Guard it with your life!
    """
    # Check for None values first to avoid TypeError in float() conversion
    if s is None:
        return (False, None)
    
    if type(s) == int or type(s) == float:
        return (True, s)

    if type(s) == bool:
        return (True, s)

    if type(s) == list:
        return (False, None)

    try:
        if type(s) == str:
            if len(s) == 0:
                return (False, None)
            
            if s[0] == "$":
                s = s[1:]
    except Exception as ee:
        traceback.print_exc()
        pass

    try:
        if s.find(",") >= 0:
            # NOTE: the locale functions in Python do not do this accurately!!!
            # TODO: consider handling (xxx) as a negative number.
            # TODO: doesn't handle scientific notation (e.g., "6.28e23" with some comma in it.)
            # TODO: doesn't handle European numbers
            if s[0] == "-":
                # negatives ok. same rules apply.
                s = s[1:]
            elif s[0] == "+":
                s = s[1:]
            # need to check for proper commas
            # first chop decimal
            decFirstPos = s.find(".")
            decLastPos = s.rfind(".")
            if decFirstPos >= 0:
                if decFirstPos != decLastPos:
                    # we have too many decimals. Maybe we're in Europe.. or maybe the string is something else.
                    return (False, "too many decimal points")

                decPos = decLastPos
                decPart = s[decPos:]
                if decPart.find(",") >= 0:
                    # we have a comma after the decimal point.
                    return (False, "comma after decimal")
                integerPart = s[:decPos]
            else:
                integerPart = s

            # print("integerPart...", integerPart)
            parts = integerPart.split(",")
            # print(parts)
            # OK the first part can be < 3
            # none of the parts can be > 3
            #
            if len(parts) > 1:
                if len(parts[0]) > 3:
                    return (False, "first part is > 3 wide")
                for i in range(1, len(parts)):
                    if len(parts[i]) != 3:
                        return (False, "part %s (%s) is != 3 wide" % (i, parts[i]))
                # ensure all are numeric
                for p in parts:
                    if not p.isnumeric():
                        return (False, "part __%s__ is not numeric" % p)

            s = s.replace(",", "")
            # print("... looking good:", parts, "-->", s)
        # endif
    except:
        traceback.print_exc()

    try:
        f = float(s)
        # print("f = ", f)
        if math.isnan(f):
            return (False, "got nan")
        if f == float("inf") or f == float("-inf"):
            # We ended up with something crazy in the conversion.
            return (False, "hit infinity")
        return (True, f)
    except ValueError as e:
        # print("CAUGHT VALUE ERROR:")
        # traceback.print_exc()
        pass
    # try:
    #    # This will actually parse a European number into an American one... not helpful.
    #    f = float(parse_decimal(s, locale='en_US'))
    #    print("f... = ", f)
    #    return (True, f)
    # except:
    #    pass
    #     try:
    #         f = parse_decimal(s, locale='de') # EU numbers
    #         return (True, f)
    #     except:
    #         pass
    return (False, None)


class FeatrixFieldBaseDetection(object):
    """Base class for feature enrichment"""

    def __init__(
        self,
        colSample,
        numUniques=-1,
        numNotNulls=-1,
        debugColName=None,
        detectorName=None,
    ):
        if numUniques == -1:
            print("missing uniques...", numUniques)
            numUniques = len(set(colSample))
        if numNotNulls == -1:
            print("missing not nulls...", numUniques)
            n = 0
            for x in colSample:
                if x == x:
                    n += 1
                numNotNulls = n

        self._numUniques = numUniques
        self._numNulls = len(colSample) - numNotNulls
        self._numNotNulls = numNotNulls
        self._debugColName = debugColName
        self.colSample = colSample  # FIXME: make a copy/
        self.type_name = detectorName
        self._confidence = 0  # Set by child's try_parsing()
        self.codec_name = "NOT SET"
        # self._casted_values = None
        self._meta_description = None
        self.sample_debug_str = "<none>"
        self.debug_info = {}
        self.has_casted_values = False
        self._casted_values = None

    def get_col_sample(self):
        try:
            d = self.colSample.value_counts().nlargest(10).to_dict()
            return d
        except TypeError:
            traceback.print_exc()       # a reminder -- and let's handle it better later.
            return None # ... don't crash here.

    def get_meta_description(self):
        return self._meta_description

    def get_debug_info(self):
        self.debug_info["numUniques"] = self._numUniques
        self.debug_info["numNotNulls"] = self._numNotNulls
        self.debug_info["numNulls"] = self._numNulls
        self.debug_info["codec_name"] = self.codec_name

        return self.debug_info

    def confidence(self):
        """Returns the confidence [0, 1] that the passed data column sample is parseable by this class."""
        return self._confidence

    def try_parsing(self):
        raise NotImplementedError("child class needs to implement try_parsing")

    def get_type_name(self):
        return self.type_name

    def get_col_name(self):
        return self._debugColName

    def free_memory(self):
        logger.info(f"---------------------------------------- {self._debugColName}: clearing casted values cache")
        self._casted_values = None
        return
    
    def cast_values(self, df_col):
        #self._casted_values = df_col
        print(f"WARNING: no cast_values implemented: {self}")
        return df_col #self._casted_values  # None means we don't need to convert anything...

    # def get_casted_values(self):
    #     #        if self._casted_values is None:
    #     #            return df_col # pass through the input.
    #     return self._casted_values

    def get_codec_name(self):
        return self.codec_name

    def is_encodeable(self):
        # print(f"... {self._debugColName} --> {self.codec_name}")
        return self.codec_name is not None



def parse_floats_properly(s):
    if s != s:
        return s
    
    if s is None:
        return s
    
    if (type(s) == float):
        return s
    
    had_vector_parts = 0
    if s[0] == "[":
        s = s[1:]
        had_vector_parts += 1
    if s[-1] == "]":
        s = s[:-1]
        had_vector_parts += 1
    if (had_vector_parts != 2):
        raise StopIteration()
    
    parts = s.split(",")
    fl = []
    for p in parts:
        try:
            fl.append(float(p))
        except ValueError as ex:
            # Don't print debug info or exit() - just raise StopIteration to indicate parsing failed
            raise StopIteration()
    
    result = torch.tensor(fl)
    return result

class FeatrixVectorEmbeddingDetection(FeatrixFieldBaseDetection):
    DETECTOR_NAME = "vector"
    def __init__(self, colSample, numUniques=-1, numNotNulls=-1, debugColName=None):
        super().__init__(
            colSample=colSample,
            numUniques=numUniques,
            numNotNulls=numNotNulls,
            debugColName=debugColName,
            detectorName="vector",
        )

        # if len(colSample) > 1_000:
        #     pass

        # print(f"colSample {len(colSample)} ... = ", colSample[:5])
        # for idx, x in enumerate(colSample):
        #     if idx > 50:
        #         break
        #     print(type(x));
        
        # self._uniques = None
        self.has_casted_values = True
        self.codec_name = "vector"

        self.num_samples = len(colSample)
        self.has_list = []

        self.best_len = []
        sampled_counts = 0

        numErrors = 0
        self._needs_cast = False
        self._casted_values = None

        for c in colSample:
            if sampled_counts > 1_000:
                self.num_samples = sampled_counts
                break
            if c != c: continue
            sampled_counts += 1
            try:
                if type(c) == list:
                    self.best_len.append(len(c))
                    self.has_list.append(True)
                elif type(c) == str:
                    try:
                        float_list = parse_floats_properly(c)
                        # print(len(float_list))
                        self.best_len.append(len(float_list))
                        self.has_list.append(True)
                    except:
                        numErrors += 1
                        self.has_list = []
            except:
                self.has_list = []
                #print("ERROR!... do we care?")
                pass    # not a list.
        # 
        # print("VECTOR RESULTS.... ")

        # if numErrors > 0:
            # print(f"{debugColName}: Vector detection: {numErrors} errors out of {len(colSample)} samples")

        self.try_parsing()

    def get_input_embedding_length(self):
        print(f"{self._debugColName} get_input_embedding_length: BEST_LEN = ", self.best_len[0])
        return self.best_len[0]

    def try_parsing(self):
        if len(self.has_list) == 0:
            self._confidence = 0
        if len(self.has_list) == self.num_samples:
            self._confidence = 1.
        else:
            if self.num_samples > 0:
                self._confidence = 0 # it's gotta be perfect or nothing. float(len(self.has_list)) / float(self.num_samples)
        # print(f"VECTOR DETECTOR --> {self._confidence}")
        return #self._casted_values

    def cast_values(self, df_col):
        logger.info(f"... VECTOR CASTING --> {self._needs_cast} -->")
        if not self._needs_cast:
            try:
                r = []
                X = df_col.to_list()
                for idx, xx in enumerate(X):
                    if xx is None or xx != xx:
                        r.append(None)
                    else:
                        r.append(torch.tensor(xx))
                return r
            except Exception as ex:
                print("ERRRRR")
                X = df_col.to_list()
                for idx, xx in enumerate(X):
                    if xx is None: print(idx)
                print("crash")
                #exit(2)
        return df_col #self._casted_values


        # print("VECTOR CASTING: getting started on... ", self._debugColName, "no casted values" if self._casted_values is None else "got something!", "length of col = ", len(df_col))
        # print(f"VECTOR CASTING {self}")   

        # if self._casted_values is not None:
        #     return self._casted_values
        # _casted_values = None
        
        # try:
        #     _casted_values = df_col.apply(parse_floats_properly)
        #     print(f"VECTOR CASTING  ... {len(_casted_values)}; {type(_casted_values[0])}")
        # except Exception as err:
        #     #traceback.print_exc()
        #     print(f"VECTOR CASTING We crashed on some nonsense that doesn't matter but let's go! [{err}]")

        # try:
        #     print("VECTOR CASTING:", self._debugColName, len(df_col))
        #     print("VECTOR CASTING:", self._debugColName, type(_casted_values[0]), len(_casted_values[0]))
        #     print("VECTOR CASTING:", self._debugColName, type(_casted_values[0][0]), _casted_values[0][0])
        # except Exception as err:
        #     print(f"VECTOR CASTING: crashed in debug prints [{err}]")

        # # print("VECTOR CASTING:", self._debugColName, _casted_values[0])
        # self._casted_values = _casted_values
        # return self._casted_values

class FeatrixFreeStringDetection(FeatrixFieldBaseDetection):
    DETECTOR_NAME = "free_string"

    def __init__(self, colSample, numUniques=-1, numNotNulls=-1, debugColName=None):
        super().__init__(
            colSample=colSample,
            numUniques=numUniques,
            numNotNulls=numNotNulls,
            debugColName=debugColName,
            detectorName="free_string",
        )
        # self._uniques = None
        self._bertEncodeLength = 8
        self.codec_name = "free_string"
        self.try_parsing()

    def get_bert_length(self):
        return self._bertEncodeLength

    def try_parsing(self):
        # We look for a large sample of strings.
        # then across the samples, do we see shared elements across delimited values?

        # number of uniques
        d = self.get_col_sample() #self.colSample.value_counts().nlargest(10).to_dict()
        if d is None:
            return
        d_total = sum(d.values())
        self.debug_info["value_counts_10_largest"] = d
        self.debug_info["value_counts_10_weight"] = d_total

        colSample = self.colSample.copy()
        colSample = colSample.dropna()
        colSample = colSample.astype("str")
        strLens = colSample.str.len()
        self.debug_info["str_len_value_counts"] = strLens.value_counts().to_dict()
        # nonzeroStrLens = strLens.nonzero()
        minStrLen = strLens.min()
        maxStrLen = strLens.max()
        theMean = strLens.mean()
        if math.isnan(theMean):
            theMean = 0
        theMedian = strLens.median()
        if math.isnan(theMedian):
            theMedian = 0
        meanStrLen = math.ceil(theMean)
        medianStrLen = math.ceil(theMedian)
        quant75StrLen = strLens.quantile(0.75)
        if math.isnan(quant75StrLen):
            quant75StrLen = 0
        stdStrLen = strLens.std()
        if math.isnan(stdStrLen):
            stdStrLen = 0

        bertMaxLength = math.ceil(meanStrLen + (2 * stdStrLen))
        # It's tempting to put a max on bertMaxLength of maxStrLen, but
        # what if our sample is a bit below reality?
        if bertMaxLength > 32:
            if meanStrLen > 32:
                bertMaxLength = min(bertMaxLength, 256)  # don't go over.
            else:
                bertMaxLength = min(bertMaxLength, 32)
        else:
            if bertMaxLength > 16:
                bertMaxLength = 32
            elif bertMaxLength > 8:
                bertMaxLength = 16
            else:
                bertMaxLength = 8
        self.debug_info["min_str_len"] = minStrLen
        self.debug_info["max_str_len"] = maxStrLen
        self.debug_info["mean_str_len"] = meanStrLen
        self.debug_info["median_str_len"] = medianStrLen
        self.debug_info["quantile75_str_len"] = quant75StrLen
        self.debug_info["std_str_len"] = stdStrLen
        self.debug_info["bertMaxLength"] = bertMaxLength

        self._bertEncodeLength = bertMaxLength
        self._confidence = (
            0.5  # if other guys are less than 50% confident, we will use this
        )
        return

    def cast_values(self, df_col):
        """Cast values for free string detection - convert to string."""
        # For free strings, we just ensure everything is string type
        _casted_values = df_col.astype(str)
        return _casted_values


# class FeatrixFieldListsOfASetDetection(FeatrixFieldBaseDetection):
#     def __init__(self, colSample, numUniques=-1, numNotNulls=-1, debugColName=None):
#         super().__init__(
#             colSample=colSample,
#             numUniques=numUniques,
#             numNotNulls=numNotNulls,
#             debugColName=debugColName,
#             detectorName="lists_of_a_set",
#         )
#         # self._uniques = None
#         self.codec_name = "lists_of_a_set"
#         self.delimiterToken = None
#         self.partsCountDict = None
#         self.try_parsing()

#     def get_meta_description(self):
#         return "delimter: __%s__; number symbols = %s" % (
#             self.delimiterToken,
#             len(self.partsCountDict),
#         )

#     def get_delimiter(self):
#         return self.delimiterToken

#     def try_parsing(self):
#         # print(self._debugColName, ": try_parsing entered")
#         # We look for a large sample of strings.
#         # then across the samples, do we see shared elements across delimited values?
#         # print("LIST OF SET: ", type(self.colSample))

#         d = self.get_col_sample() #self.colSample.value_counts().nlargest(10).to_dict()
#         if d is None:
#             return

#         d_total = sum(d.values())
#         self.debug_info["value_counts_10_largest"] = d
#         self.debug_info["value_counts_10_weight"] = d_total

#         _uniques = set(self.colSample[self.colSample.notnull()].astype(str))

#         lenUniques = len(_uniques)

#         delimiterList = [",", ";", "-", "/"]  # " ", 31 Oct 2023 -- removing space for now.
#         delimitResults = {}

#         fullPartsCount = {}

#         for d in delimiterList:
#             numPartsDict = {}
#             totalGroups = 0
#             groupsOfThree = 0  # if there's a lot of these, probably a scalar.

#             partsCount = {}
#             # explodedParts = []
#             for v in _uniques:
#                 if type(v) != str:
#                     continue
#                 if v == "" or v.isspace():
#                     continue
#                 if d == ",":
#                     if len(v) > 3:
#                         if (
#                             v[0] == "$"
#                         ):  # HACK: cutting off $ on numbers for 3s counting.
#                             v = v[1:]
#                 parts = v.split(d)

#                 existing = numPartsDict.get(len(parts), 0)
#                 numPartsDict[len(parts)] = existing + 1

#                 if d == ",":
#                     lastPart = parts[-1]
#                     decPos = lastPart.find(".")
#                     if decPos > 0:  # HACK: cut off decimal point of end
#                         lastPart = lastPart[0:decPos]
#                         parts[-1] = lastPart
#                     # print(parts)
#                 for p in parts:
#                     p_trim = p.strip()
#                     existing = partsCount.get(p_trim, 0)
#                     partsCount[p_trim] = existing + 1

#                     totalGroups += 1
#                     if d == ",":
#                         if len(p) == 3 and p.isnumeric():
#                             groupsOfThree += 1
#                     # endif
#                 # endfor
#             # endfor

#             # if self._debugColName == "Title" and d == " ":
#             #    print("... partsCount = ", len(partsCount))
#             # print(d, ": TOTAL GROUPS = ", totalGroups, "; THREEs = ", groupsOfThree)

#             # FIXME: if groupsOfThree > 1/3rd of totalGroups, it's probably a number.
#             # FIXME: this is all crazy bad. :-) Locales, etc.

#             # if they are all length 1, it's not a list.
#             if numPartsDict.get(1, 0) >= (lenUniques * 0.5):
#                 continue
#             # print(self._debugColName, ": ", "'%s'" % d, ": numPartsDict = ", numPartsDict)
#             # if True and self._debugColName == "Title":
#             ##    for k, v in partsCount.items():
#             #        if v > 5:
#             #            print(k, "-->", v)
#             #            print(partsCount)

#             if groupsOfThree >= (0.33 * lenUniques):
#                 continue  # print("lists of a set -- LOOKS LIKE A SCALAR! -- ignoring")
#             else:
#                 # or more simply... if the num unique parts is < 0.5% of the uniques?

#                 numUniqueParts = len(partsCount)
#                 # print("numUniqueParts = ", numUniqueParts)
#                 # If we have a high number of unique parts
#                 if numUniqueParts > len(_uniques):
#                     # we have more unique parts than we have combinations --> no reduction of entropy here.
#                     reductionRatio = 0
#                 else:
#                     # We want to drive a low number of uniques (away from the unique combos) higher
#                     # so we do 1.0 - ratio
#                     reductionRatio = 1.0 - (float(numUniqueParts) / float(lenUniques))
#                 delimitResults[d] = reductionRatio
#                 fullPartsCount[d] = partsCount

#             # endif

#         #
#         # if self._debugColName == "Title":
#         #    print("lenUniques... = ", lenUniques)
#         #    print(self.colSample)

#         self._confidence = 0.0

#         if len(delimitResults) > 0:
#             maxValue = max(delimitResults.values())
#             for k, v in delimitResults.items():
#                 # print("try_parsing: RESULTS: ", v, maxValue)
#                 if v == maxValue:
#                     # print("try_parsing: SETTING...")
#                     self.delimiterToken = k
#                     self.partsCountDict = fullPartsCount.get(k)
#                     self._confidence = v
#                     break
#         # print("try_parsing: token = ", self.delimiterToken, "; confidence = ", self._confidence)
#         # print(delimitResults)
#         # print("try_parsing: @@@@@@@", self)
#         # print("try_parsing: delimiterToken...", self.delimiterToken)
#         # print("try_parsing: partsCountDict...", self.partsCountDict)

#         self.debug_info["delimitResults"] = delimitResults
#         self.debug_info["fullPartsCount"] = fullPartsCount
#         return

#     def cast_values(self, df_col):
#         _casted_values = df_col.astype(str)
#         return _casted_values       # XXX?????
#         # return []

#         #
#         # A lot of overlap with the codec part of this.
#         #
#         # Should the codecs take in help from the detector, or should the
#         # detector leverage the codec to try to capture a representation?
#         #

#         # print("cast_values: @@@@@@@", self)
#         if self._casted_values is not None:
#             print(">>> Warning: called cast_values() again")

#         assert self.partsCountDict is not None, "no parts dictionary"
#         assert self.delimiterToken is not None, "no delimter set?!"

#         X = []
#         self._casted_values = df_col.astype(str)

#         maxLen = 0
#         # now process them.
#         for idx, val in self._casted_values.items():
#             if val == "nan":
#                 parts = [np.nan]
#             else:
#                 parts = val.split(self.delimiterToken)
#                 parts.sort()
#             maxLen = max(maxLen, len(parts))
#             X.append(parts)
#         for i in range(len(X)):
#             xi = X[i]
#             while len(xi) < maxLen:
#                 xi.append(np.nan)
#             X[i] = xi
#         # x = OneHotEncoder().fit_transform(X).toarray()
#         # self._casted_values = x
#         print("CASTED_VALUES SIZE = ", sys.getsizeof(self._casted_values))
#         print()
#         return self._casted_values


class FeatrixFieldSetDetection(FeatrixFieldBaseDetection):
    DETECTOR_NAME = "set"

    def __init__(self, colSample, numUniques=-1, numNotNulls=-1, debugColName=None):
        super().__init__(
            colSample=colSample,
            numUniques=numUniques,
            numNotNulls=numNotNulls,
            debugColName=debugColName,
            detectorName="set",
        )
        # self._uniques = None
        self.try_parsing()
        self.codec_name = "set"

    def get_meta_description(self):
        return "number symbols = %s" % self._numUniques

    def try_parsing(self):
        # self._uniques = set(self.colSample[self.colSample.notnull()])
        # lenUniques = len(self._uniques)
        # lenSamples = len(self.colSample)
        lenUniques = self._numUniques
        lenSamples = self._numNotNulls  # len(self.colSample)
        # print(f"DETECT SET: {self._debugColName} -- {lenUniques} vs {lenSamples}")

        # CRITICAL: Reject numeric columns with HIGH cardinality - they should be SCALAR, not SET
        # A SET can have numeric values (like ratings 1-5), but if it has many unique numeric values,
        # it's likely a continuous numeric column that should be SCALAR
        # Sample values to check if they're numeric
        NUM_ROWS_TO_CHECK = min(1000, len(self.colSample))
        try:
            s_replace = self.colSample[self.colSample.notnull()]
            NUM_ROWS_TO_CHECK = min(NUM_ROWS_TO_CHECK, len(s_replace))
            theSample = s_replace.sample(NUM_ROWS_TO_CHECK) if NUM_ROWS_TO_CHECK > 0 else s_replace
        except:
            theSample = self.colSample[self.colSample.notnull()]
            NUM_ROWS_TO_CHECK = min(1000, len(theSample))
        
        if NUM_ROWS_TO_CHECK > 0:
            numericCount = 0
            for v in theSample:
                isNumber, _ = _isNumber(v)
                if isNumber:
                    numericCount += 1
            
            # If >80% of values are numeric AND we have high cardinality (many unique values),
            # this should be SCALAR, not SET
            numericRatio = float(numericCount) / float(NUM_ROWS_TO_CHECK)
            if numericRatio > 0.8:
                # High cardinality threshold: if unique values > 10% of samples, it's likely continuous numeric
                # Low cardinality numeric sets (like ratings 1-5) will have few uniques and pass through
                cardinalityRatio = float(lenUniques) / float(lenSamples) if lenSamples > 0 else 0.0
                if cardinalityRatio > 0.1:  # More than 10% unique = high cardinality = should be SCALAR
                    self._confidence = 0.0  # Reject - should be scalar
                    return

        lenSamplesFactor = 0.001
        if lenSamples < 10_000:
            lenSamplesFactor = 0.01
        elif lenSamples < 1_000:
            lenSamplesFactor = 0.1
            
        if lenUniques < (lenSamples * lenSamplesFactor):
                self._confidence = 1.0

        elif lenUniques < (lenSamples *lenSamplesFactor):
            self._confidence = 0.9

        elif lenUniques < (lenSamples * lenSamplesFactor):
            self._confidence = 0.75

        if lenSamples < 20:
            if lenUniques < (lenSamples * 0.3):
                self._confidence = 0.51

        #        self._confidence = 1.0  else 0.0
        return

    def cast_values(self, df_col):
        # if self._casted_values is not None:
        #     print(">>> Warning: called cast_values() again")

        _casted_values = df_col.astype(str)
        return _casted_values


class FeatrixFieldTimeDetection(FeatrixFieldBaseDetection):
    DETECTOR_NAME = "timestamp"

    def __init__(self, colSample, numUniques=-1, numNotNulls=-1, debugColName=None):
        super().__init__(
            colSample=colSample,
            numUniques=numUniques,
            numNotNulls=numNotNulls,
            debugColName=debugColName,
            detectorName=FeatrixFieldTimeDetection.DETECTOR_NAME,
        )
        self.try_parsing()
        # print("... colSample = ", colSample)
        self._casted_values = None
        # Set codec_name to "timestamp" if detection was successful
        if self._confidence > 0:
            self.codec_name = "timestamp"
        else:
            self.codec_name = None

    def try_parsing(self):
        NUM_ROWS_TO_CHECK = 100
        # FIXME: bug if there's < 100 samples...
        # if len(self.colSample) < NUM_ROWS_TO_CHECK:
        #    NUM_ROWS_TO_CHECK = len(self.colSample[self.colSample.notnull()]) - 1
        # print("NUM_ROWS_TO_CHECK = ", NUM_ROWS_TO_CHECK)
        # print(self.colSample)
        try:
            s_replace = (
                self.colSample
            )  # .replace(['NaN', 'None', '', 'nan'], float('nan'))
            s_replace = s_replace[s_replace.notnull()]
            NUM_ROWS_TO_CHECK = min(NUM_ROWS_TO_CHECK, len(s_replace))
            theSample = s_replace.sample(NUM_ROWS_TO_CHECK)
        except:
            # Sometimes we crash if there's not enough data.
            traceback.print_exc()
            print("CRASH...")
            theSample = self.colSample

        if len(theSample) == 0:
            return

        #        print("theSample ... = ", theSample)
        ts_list = []
        for v in theSample:
            isNumber, vv = _isNumber(v)
            # if it's just a number... probably not a time unless it is a unix timestamp...
            # so for unix timestamps, we need to assume maybe a recent or near-future time?
            if not isNumber:
                try:
                    # XXX: send in a default datetime ; try to connect / or limit
                    # XXX: detect that this is just a timefield by virtue of a fewer number
                    # XXX: of elements and we only change the time and not date parts
                    # XXX: I don't think we have to try to connect time fields with their
                    # XXX: corresponding date fields right now anyway.
                    default_datetime = datetime.fromtimestamp(0)

                    parsedTime = DateUtilParse(
                        v, default=default_datetime
                    )  # I _have_ seen this crash before.
                    if parsedTime is not None:
                        ts_list.append(parsedTime)
                except Exception:
                    pass
                    # ts_list.append(None)
        # print(self._debugColName, ": ts_list... = ", ts_list)
        # print(self._debugColName, ":... sample  = ", list(theSample))
        # print()
        # if len(ts_list) >= (NUM_ROWS_TO_CHECK / 2):
        # looking good.
        if NUM_ROWS_TO_CHECK > 0:
            self._confidence = float(len(ts_list)) / float(NUM_ROWS_TO_CHECK)
        # endif
        return

    def cast_values(self, df_col):
        # if self._casted_values is not None:
        #     print(">>> Warning: called cast_values() again")

        _casted_values = pd.to_datetime(
            df_col, errors="coerce"
        )
        return _casted_values


class FeatrixFieldTimeIntervalDetection(FeatrixFieldBaseDetection):
    DETECTOR_NAME = "time_interval"

    def __init__(self, colSample, numUniques=-1, numNotNulls=-1, debugColName=None):
        super().__init__(
            colSample=colSample,
            numUniques=numUniques,
            numNotNulls=numNotNulls,
            debugColName=debugColName,
            detectorName=FeatrixFieldTimeIntervalDetection.DETECTOR_NAME,
        )
        self.try_parsing()
        # print("... colSample = ", colSample)
        self._casted_values = None
        self.codec_name = None

    def try_parsing(self):
        NUM_ROWS_TO_CHECK = 100
        # FIXME: bug if there's < 100 samples...
        # if len(self.colSample) < NUM_ROWS_TO_CHECK:
        #    NUM_ROWS_TO_CHECK = len(self.colSample[self.colSample.notnull()]) - 1
        # print("NUM_ROWS_TO_CHECK = ", NUM_ROWS_TO_CHECK)
        # print(self.colSample)
        try:
            s_replace = (
                self.colSample
            )  # .replace(['NaN', 'None', '', 'nan'], float('nan'))
            s_replace = s_replace[s_replace.notnull()]
            NUM_ROWS_TO_CHECK = min(NUM_ROWS_TO_CHECK, len(s_replace))
            theSample = s_replace.sample(NUM_ROWS_TO_CHECK)
        except:
            # Sometimes we crash if there's not enough data.
            traceback.print_exc()
            print("CRASH...")
            theSample = self.colSample

        if len(theSample) == 0:
            return

        #        print("theSample ... = ", theSample)
        ts_list = []
        for v in theSample:
            isNumber, vv = _isNumber(v)
            # if it's just a number... probably not a time unless it is a unix timestamp...
            # so for unix timestamps, we need to assume maybe a recent or near-future time?
            if not isNumber:
                try:
                    seconds = DateIntervalParse(v)
                    if not isnan_or_null_no_crash(
                        seconds
                    ):  # is not None or math.isnan():
                        ts_list.append(seconds)
                except Exception:
                    pass

        if NUM_ROWS_TO_CHECK > 0:
            self._confidence = float(len(ts_list)) / float(NUM_ROWS_TO_CHECK)
        # endif
        return

    def cast_values(self, df_col):
        # if self._casted_values is not None:
        #     print(">>> Warning: called cast_values() again")

        def wrap_parse(v):
            try:
                if type(v) == float:
                    return v
                return DateIntervalParse(v)
            except:
                print(f"ERROR PARSING POSSIBLE TIME INTERVAL: v = __{v}")
                traceback.print_exc()
            return None

        # Pandas DOES have a to_timedelta()
        _casted_values = df_col.map(lambda v: wrap_parse(v))
        return _casted_values




class FeatrixEmailDetection(FeatrixFieldBaseDetection):
    DETECTOR_NAME = "email"

    def __init__(self, colSample, numUniques=-1, numNotNulls=-1, debugColName=None):
        super().__init__(
            colSample=colSample,
            numUniques=numUniques,
            numNotNulls=numNotNulls,
            debugColName=debugColName,
            detectorName="email",
        )
        # self._uniques = None
        # Enrichment removed - encode email columns as strings
        self.codec_name = "free_string"
        self.delimiterToken = None
        self.partsCountDict = None
        self.try_parsing()

    # def get_meta_description(self):
    #     return "delimter: __%s__; number symbols = %s" % (self.delimiterToken, len(self.partsCountDict))

    # def get_delimiter(self):
    #     return self.delimiterToken

    def try_parsing(self):
        # print("try_parsing entered")

        _uniques = None
        try:
            _uniques = list(set(self.colSample[self.colSample.notnull()].astype(str)))
        except:
            traceback.print_exc()
            return
        
        # s_replace = self.colSample  # .replace(['NaN', 'None', '', 'nan'], float('nan'))
        # s_replace = s_replace[s_replace.notnull()]
        # NUM_ROWS_TO_CHECK = min(NUM_ROWS_TO_CHECK, len(s_replace))
        # theSample = s_replace.sample(NUM_ROWS_TO_CHECK)

        # pick 100.
        NUM_ROWS_TO_CHECK = min(len(_uniques), 100)

        sample = random.sample(_uniques, NUM_ROWS_TO_CHECK)

        foundEmails = []

        for s in sample:
            s = str(s)
            atPos = s.find("@")
            if atPos < 0:
                continue
            userPart = s[0:atPos]
            domainPart = s[atPos + 1 :]

            if len(userPart) <= 0 or len(domainPart) <= 0:
                continue  # nothing before or after the @

            if domainPart.find("@") >= 0:
                continue  # two @s

            if domainPart.find(".") > 0:
                # looks good.
                # this is superficial, but we matched a <token>@<token>. [and presumably another <token> later but who cares]
                foundEmails.append([s, userPart, domainPart])
        # endfor

        # print("FOUND EMAILS:")
        # for f in foundEmails:
        #     print(f)
        if NUM_ROWS_TO_CHECK > 0:
            self._confidence = float(len(foundEmails)) / float(NUM_ROWS_TO_CHECK)
        return

    def cast_values(self, df_col):
        """Cast values for email detection - convert to string."""
        # For emails, we just ensure everything is string type
        _casted_values = df_col.astype(str)
        return _casted_values


class FeatrixDomainNameDetection(FeatrixFieldBaseDetection):
    DETECTOR_NAME = "domain_name"

    def __init__(self, colSample, numUniques=-1, numNotNulls=-1, debugColName=None):
        super().__init__(
            colSample=colSample,
            numUniques=numUniques,
            numNotNulls=numNotNulls,
            debugColName=debugColName,
            detectorName="domain_name",
        )
        # self._uniques = None
        self.codec_name = "domain_name"  # Use domain codec
        self.delimiterToken = None
        self.partsCountDict = None
        self.try_parsing()

    # def get_meta_description(self):
    #     return "delimter: __%s__; number symbols = %s" % (self.delimiterToken, len(self.partsCountDict))

    # def get_delimiter(self):
    #     return self.delimiterToken

    def try_parsing(self):
        # print("try_parsing entered")

        _uniques = None
        try:
            _uniques = list(set(self.colSample[self.colSample.notnull()].astype(str)))
        except:
            traceback.print_exc()
            return
        
        # s_replace = self.colSample  # .replace(['NaN', 'None', '', 'nan'], float('nan'))
        # s_replace = s_replace[s_replace.notnull()]
        # NUM_ROWS_TO_CHECK = min(NUM_ROWS_TO_CHECK, len(s_replace))
        # theSample = s_replace.sample(NUM_ROWS_TO_CHECK)

        # pick 100.
        NUM_ROWS_TO_CHECK = min(len(_uniques), 100)

        sample = random.sample(_uniques, NUM_ROWS_TO_CHECK)

        foundDomains = []

        for s in sample:
            s = str(s)
            # If it has an @, it's an email not a domain
            if s.find('@') >= 0:
                continue
            
            if s.startswith("http://"):
                s = s[len("http://"):]
            elif s.startswith("https://"):
                s = s[len("https://"):]
            
            atPos = s.find(".")
            if atPos < 0:
                continue
            firstPart = s[0:atPos]
            secondPart = s[atPos + 1 :]

            if len(firstPart) <= 0 or len(secondPart) <= 0:
                continue  # nothing before or after the @

            if firstPart == "www":
                foundDomains.append(s)
                continue  # two @s
            if secondPart in ["com", "org", "net", "gov", "edu"]:
                foundDomains.append(s)
        # endfor

        # print("FOUND EMAILS:")
        # for f in foundEmails:
        #     print(f)
        if NUM_ROWS_TO_CHECK > 0:
            self._confidence = float(len(foundDomains)) / float(NUM_ROWS_TO_CHECK)
        return


class FeatrixURLDetection(FeatrixFieldBaseDetection):
    """
    Detector for URL/domain columns.
    Detects URLs with protocols, paths, query params.
    """
    DETECTOR_NAME = "url"

    def __init__(self, colSample, numUniques=-1, numNotNulls=-1, debugColName=None):
        super().__init__(
            colSample=colSample,
            numUniques=numUniques,
            numNotNulls=numNotNulls,
            debugColName=debugColName,
            detectorName="url",
        )
        self.codec_name = "url"
        self.try_parsing()

    def try_parsing(self):
        """Detect URLs by looking for URL patterns."""
        _uniques = None
        try:
            _uniques = list(set(self.colSample[self.colSample.notnull()].astype(str)))
        except:
            traceback.print_exc()
            return
        
        NUM_ROWS_TO_CHECK = min(len(_uniques), 100)
        sample = random.sample(_uniques, NUM_ROWS_TO_CHECK)

        foundURLs = []

        for s in sample:
            s = str(s).strip()
            
            # Strong URL indicators
            has_protocol = (s.startswith("http://") or s.startswith("https://") or 
                           s.startswith("ftp://") or s.startswith("ftps://") or
                           s.startswith("ws://") or s.startswith("wss://"))
            
            # Check for path or query string (indicators it's a URL not just domain)
            has_path = "/" in s and not s.endswith("/")
            has_query = "?" in s
            has_fragment = "#" in s
            
            # Check for domain-like structure
            has_dot = "." in s
            
            # If it has protocol, it's likely a URL
            if has_protocol:
                foundURLs.append(s)
                continue
            
            # If it has path/query/fragment + domain structure, likely URL
            if (has_path or has_query or has_fragment) and has_dot:
                # Make sure it's not an email
                if "@" not in s:
                    foundURLs.append(s)
                    continue
            
            # Check for common URL patterns without protocol
            # (e.g., "www.example.com/path" or "api.service.com/v1/endpoint")
            if has_dot and (has_path or has_query):
                # Avoid email addresses
                if "@" not in s:
                    foundURLs.append(s)
        
        # Calculate confidence
        if NUM_ROWS_TO_CHECK > 0:
            self._confidence = float(len(foundURLs)) / float(NUM_ROWS_TO_CHECK)
        return
    
    def get_codec_name(self):
        """Return codec name for URL columns."""
        return "url"
    
    def get_casted_column_values(self, df_col):
        """Cast column values to strings for URL encoding."""
        _casted_values = df_col.astype(str)
        return _casted_values

    def cast_values(self, df_col):
        """Cast values for domain name detection - convert to string."""
        # For domain names, we just ensure everything is string type
        _casted_values = df_col.astype(str)
        return _casted_values

def df_isNumberWrapper(f):
    (worked, _f) = _isNumber(f)
    if worked:
        return _f
    return np.nan


class FeatrixFieldScalarDetection(FeatrixFieldBaseDetection):
    def __init__(self, colSample, numUniques=-1, numNotNulls=-1, debugColName=None):
        super().__init__(
            colSample=colSample,
            numUniques=numUniques,
            numNotNulls=numNotNulls,
            debugColName=debugColName,
            detectorName="scalar",
        )
        self.try_parsing()
        self.codec_name = "scalar"
        self.sample_debug_str = None

    def try_parsing(self):
        NUM_ROWS_TO_CHECK = min(100, len(self.colSample))
        try:
            s_replace = (
                self.colSample
            )  # .replace(['NaN', 'None', '', 'nan'], float('nan'))
            s_replace = s_replace[s_replace.notnull()]
            NUM_ROWS_TO_CHECK = min(NUM_ROWS_TO_CHECK, len(s_replace))
            theSample = s_replace.sample(NUM_ROWS_TO_CHECK)

            # theSample = self.colSample[self.colSample.as_type('float32').notnull()].as_type('float32').sample(NUM_ROWS_TO_CHECK)
            # NUM_ROWS_TO_CHECK = min(len(theSample), NUM_ROWS_TO_CHECK)
        except:
            theSample = self.colSample
            NUM_ROWS_TO_CHECK = len(self.colSample)

        # print(f"{self._debugColName}.... NUM_ROWS_TO_CHECK = {NUM_ROWS_TO_CHECK}")
        numberCount = 0

        adjustedSampleCount = NUM_ROWS_TO_CHECK
        dollarSigns = 0
        nanStrCount = 0
        for v in theSample:
            if type(v) == str:
                if v == "":
                    v = np.nan
                elif v[0] == "$":
                    dollarSigns += 1
                    v = v[1:]
                elif v == "nan":
                    nanStrCount += 1
                    # print(f"{nanStrCount}/{NUM_ROWS_TO_CHECK}: got a nan str; grrrr")
                    v = np.nan
                    # this shouldn't even be in the sample.
                    adjustedSampleCount -= 1
                    continue
            isNumber, vv = _isNumber(v)

            if isNumber:
                numberCount += 1

        if adjustedSampleCount == 0:
            # well crap.
            self.sample_debug_str = "all the samples were 'nan' strings or something. Looks bad. Please debug more."
            adjustedSampleCount = NUM_ROWS_TO_CHECK

        # print("dollarSigns... = ", self._debugColName, dollarSigns)
        if adjustedSampleCount > 0:
            self._confidence = float(numberCount) / float(adjustedSampleCount)

        self.sample_debug_str = (
            "... sample = %s; numberCount = %d; adjustedSampleCount = %d"
            % (list(theSample), numberCount, adjustedSampleCount)
        )
        # print("....", self._debugColName, self.sample_debug_str)
        # print("confidence..", self._debugColName, self._confidence)
        return

    def cast_values(self, df_column):
        # columnName = self.get_col_name()
        # if self._casted_values is not None:
        #     print(">>> Warning: called cast_values() again")

        _casted_values = df_column.transform(lambda x: df_isNumberWrapper(x))
        return _casted_values


class FeatrixJsonDetection(FeatrixFieldBaseDetection):
    DETECTOR_NAME = "json"
    
    def __init__(self, colSample, numUniques=-1, numNotNulls=-1, debugColName=None):
        super().__init__(
            colSample=colSample,
            numUniques=numUniques,
            numNotNulls=numNotNulls,
            debugColName=debugColName,
            detectorName="json",
        )
        self.codec_name = "json"
        self.try_parsing()
    
    def _safe_parse_dict_like(self, value: str):
        """Safely parse dict-like strings."""
        import json
        import ast
        import re
        
        if not isinstance(value, str):
            return None
            
        value = value.strip()
        if not (value.startswith('{') and value.endswith('}')):
            return None
        
        # Try standard JSON parsing
        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Try ast.literal_eval for Python dict literals
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, dict):
                return parsed
        except (ValueError, SyntaxError):
            pass
        
        return None
    
    def _safe_parse_list_of_dicts(self, value: str):
        """Safely parse list-of-dicts strings."""
        import json
        import ast
        
        if not isinstance(value, str):
            return None
            
        value = value.strip()
        if not (value.startswith('[') and value.endswith(']')):
            return None
        
        # Try standard JSON parsing
        try:
            parsed = json.loads(value)
            if isinstance(parsed, list) and len(parsed) > 0:
                if all(isinstance(item, dict) for item in parsed):
                    return parsed
        except (json.JSONDecodeError, TypeError):
            pass
        
        # Try ast.literal_eval for Python list literals
        try:
            parsed = ast.literal_eval(value)
            if isinstance(parsed, list) and len(parsed) > 0:
                if all(isinstance(item, dict) for item in parsed):
                    return parsed
        except (ValueError, SyntaxError):
            pass
        
        return None
    
    def try_parsing(self):
        """Detect JSON by checking if values are parseable as dicts or lists of dicts."""
        NUM_ROWS_TO_CHECK = min(100, len(self.colSample))
        try:
            s_replace = self.colSample[self.colSample.notnull()]
            NUM_ROWS_TO_CHECK = min(NUM_ROWS_TO_CHECK, len(s_replace))
            theSample = s_replace.sample(NUM_ROWS_TO_CHECK)
        except:
            theSample = self.colSample
            NUM_ROWS_TO_CHECK = len(self.colSample)
        
        if NUM_ROWS_TO_CHECK == 0:
            self._confidence = 0.0
            return
        
        json_count = 0
        for v in theSample:
            if not isinstance(v, str):
                continue
            
            # Check for dicts
            parsed_dict = self._safe_parse_dict_like(v)
            if parsed_dict is not None:
                json_count += 1
                continue
            
            # Check for lists of dicts
            parsed_list = self._safe_parse_list_of_dicts(v)
            if parsed_list is not None:
                json_count += 1
                continue
        
        if NUM_ROWS_TO_CHECK > 0:
            self._confidence = float(json_count) / float(NUM_ROWS_TO_CHECK)
        else:
            self._confidence = 0.0
    
    def get_codec_name(self):
        """Return codec name for JSON columns."""
        return "json"
    
    def cast_values(self, df_col):
        """Cast values for JSON - keep as strings since we'll parse during encoding."""
        return df_col.astype(str)


# The order in this list matters! <-- Pay attention folks!
DetectorList = [
    FeatrixFieldScalarDetection,
    FeatrixFieldSetDetection,
    FeatrixFieldTimeDetection,
    FeatrixFieldTimeIntervalDetection,
    # FeatrixFieldListsOfASetDetection,
    FeatrixEmailDetection,
    FeatrixURLDetection,           ## Check URLs before domains (more specific)
    FeatrixDomainNameDetection,
    FeatrixVectorEmbeddingDetection,
    FeatrixJsonDetection,          ## Check JSON before free string (more specific)
    FeatrixFreeStringDetection     ## KEEP AT END
]

DetectorDict = {
    ColumnType.SCALAR: FeatrixFieldScalarDetection,
    ColumnType.SET: FeatrixFieldSetDetection,
    ColumnType.TIMESTAMP: FeatrixFieldTimeDetection,
    # ColumnType.LIST_OF_SETS: FeatrixFieldListsOfASetDetection,
    ColumnType.FREE_STRING: FeatrixFreeStringDetection,
    ColumnType.EMAIL: FeatrixEmailDetection,
    ColumnType.DOMAIN: FeatrixDomainNameDetection,
    ColumnType.VECTOR: FeatrixVectorEmbeddingDetection,
    ColumnType.JSON: FeatrixJsonDetection
}

DetectorStrDict = {
    "scalar": FeatrixFieldScalarDetection,
    "set": FeatrixFieldSetDetection,
    "timestamp": FeatrixFieldTimeDetection,
    # "lists_of_a_set": FeatrixFieldListsOfASetDetection,
    "free_string": FeatrixFreeStringDetection,
    "email": FeatrixEmailDetection,
    "domain_name": FeatrixDomainNameDetection,
    "vector": FeatrixVectorEmbeddingDetection,
    "json": FeatrixJsonDetection,
}


if __name__ == "__main__":
    import random
    import time

    s = "5112"
    ret = _isNumber(s)
    assert ret[0] == True, "isNumber must return True for non-delimited numbers."
    # print(ret)

    s = "51,12"
    ret = _isNumber(s)
    # print(ret)
    assert ret[0] == False, "isNumber must return False for badly delimited numbers."
    # print(ret)

    s = "511210,513210,561311,713"
    ret = _isNumber(s)
    assert ret[0] == False, "isNumber must return False for badly delimited numbers."
    # print(ret)

    s = "511,210,513,210,561,311,713"
    ret = _isNumber(s)
    assert ret[0] == True, "isNumber must return True for properly delimited numbers"
    # print(ret)

    s = "511,210,513,210.561,311,713"
    ret = _isNumber(s)
    assert (
        ret[0] == False
    ), "isNumber must return False for badly delimited numbers [comma after decimal]."
    # print(ret)

    # get some timestamps.
    timeNow = time.time()
    timeRange = 30 * 86400
    timeList = []
    for i in range(200):
        this_ts = timeNow - random.randint(0, timeRange)
        if random.randint(0, 100) > 70:
            timeList.append(None)
        else:
            timeList.append(str(datetime.fromtimestamp(this_ts)))

    # print(timeList)

    df = pd.DataFrame(timeList)
    # print(df)

    print(df.columns)
    fftd = FeatrixFieldTimeDetection(df[df.columns[0]], debugColName="test_time")
    print("....")
    print(fftd.confidence())

    ffscalar = FeatrixFieldScalarDetection(
        df[df.columns[0]], debugColName="scalar-vals"
    )
    print(ffscalar.confidence())

    ffset = FeatrixFieldSetDetection(df[df.columns[0]], debugColName="set-vals")
    print(ffset.confidence())
