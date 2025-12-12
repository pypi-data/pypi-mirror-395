#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2024 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#
import math
import random
import traceback
import logging
import re
from datetime import datetime

import numpy as np
import pandas as pd
import scipy.stats as SS

from featrix.neural.detect import FeatrixEmailDetection
from featrix.neural.detect import FeatrixFieldSetDetection
from featrix.neural.detect import FeatrixFieldTimeDetection
from featrix.neural.detect import FeatrixFieldTimeIntervalDetection
from featrix.neural.detect import FeatrixFreeStringDetection
from featrix.neural.detect import FeatrixDomainNameDetection

logger = logging.getLogger(__name__)


class FeatrixFieldBaseEnrichment(object):
    """Base class for feature enrichment"""

    def __init__(self, detector):
        self._detector = detector  # FIXME: make a copy?
        self.enriched_df = pd.DataFrame()

    def enrich(self, column):
        """Expand the column into interesting parts."""
        raise NotImplementedError("subclass needs to implement this!")

    def format_new_col_name(self, suffix):
        columnName = self._detector.get_col_name()
        assert columnName is not None, "need column name to enrich new columns"
        return f"{self.get_col_name()}_featrix_untie_{suffix}"

    def get_col_name(self):
        assert self._detector is not None
        return self._detector.get_col_name()

    def looks_interesting(self, enriched_name):
        """Returns true if the enriched column looks interesting"""
        raise NotImplementedError("subclass needs to implement this!")

    def get_enriched_names(self):
        # print("get_enriched_names called on ", self)
        return self.enriched_df.columns.values

    def get_enriched_data(self, name):
        return self.enriched_df[name]

    def keep_original_column(self):
        """Override to NOT keep the original column for encoding if the new columns replace it."""
        return True




class FeatrixFieldEmailEnrichment(FeatrixFieldBaseEnrichment):
    def __init__(self, detector):
        super().__init__(detector=detector)
        self.email_user_col = None
        self.email_domain_col = None

    def looks_interesting(self, enriched_name):
        """Returns true if the enriched column looks interesting"""
        # all uniques? No
        # FIXME: we want some cross-entropy or predictive power assessment on these fields.
        # FIXME: this is pretty dumb.
        # print("looks_interesting on %s called" % enriched_name)
        data_col = self.enriched_df[enriched_name]
        data = data_col[data_col.notnull()]

        # If we are super unique, it's not going to bring much value
        # FIXME: the .95 really should be controllable (prob by the user)
        if len(data.unique()) >= (len(data) * 0.95):
            return False

        try:
            logger.info(f"Checking entropy of value counts: {data.value_counts()}")
            entropy = SS.entropy(data.value_counts(), base=2)
            logger.info(f"Entropy is {entropy}")
            # norm = entropy / float(dataLen)
            # print("norm entropy: ", entropy, norm)
            if entropy < 1:
                return False
        except Exception as e:  # noqa
            logger.error(f"Calculating entropy crashed with {e}")
            # Catch entropy() crashes.
            traceback.print_exc()

        return True

    def enrich(self, column):
        """Expand the column into interesting parts."""
        _start = datetime.now()
        assert self._detector is not None

        new_col_user = self.format_new_col_name("email_user")
        new_col_domain = self.format_new_col_name("email_domain")
        # Split the email to user/domain, and set to nan anything bad email address -- for now that would be
        # no input, an empty string, or if there are multiple @'s in the address. We figure out invalids for
        # the user column using both columns (if either is broken, they both go to nan) and carry that into
        # the domain column as well.
        self.enriched_df[[new_col_user, new_col_domain]] = column.str.split('@', n=1, expand=True)
        self.enriched_df.loc[
            pd.isna(self.enriched_df[new_col_user]) |
            pd.isna(self.enriched_df[new_col_domain]) |
            (self.enriched_df[new_col_user].str.len() == 0) |
            (self.enriched_df[new_col_domain].str.len() == 0) |
            (self.enriched_df[new_col_domain].str.contains('@') is True),
            new_col_user
        ] = np.nan
        self.enriched_df.loc[
            pd.isna(self.enriched_df[new_col_user]),
            new_col_domain
        ] = np.nan
        # We don't really care about the user -- but for now leverage the above check to help use weed out
        # data using both user/domain after the split
        self.enriched_df.drop(new_col_user, axis=1, inplace=True)

        # self.enriched_df[new_col_user] = np.nan
        # self.enriched_df[new_col_domain] = np.nan

        # logger.info("Start enriching of columns for email column...")
        # for idx, s in column.items():
        #     s = str(s)
        #     atPos = s.find("@")
        #     if atPos < 0:
        #         continue
        #     userPart = s[0:atPos]
        #     domainPart = s[atPos + 1 :]
        #
        #     if len(userPart) <= 0 or len(domainPart) <= 0:
        #         continue  # nothing before or after the @
        #
        #     if domainPart.find("@") >= 0:
        #         continue  # two @s
        #
        #     if domainPart.find(".") > 0:
        #         # looks good.
        #         # this is superficial, but we matched a <token>@<token>. [and presumably another <token> later but who cares]
        #         self.enriched_df.at[idx, new_col_user] = userPart
        #         self.enriched_df.at[idx, new_col_domain] = domainPart
        #
        #     if (idx % 1000) == 0:
        #         logger.info(f"...email enrichment idx {idx}, timeer {(datetime.now() - _start).total_seconds()} seconds")
        # endfor

        return self.enriched_df


class FeatrixFieldDomainEnrichment(FeatrixFieldBaseEnrichment):
    """ FIXME: We don't have anything enriching domain names yet """
    def __init__(self, detector):
        super().__init__(detector=detector)

    def looks_interesting(self, enriched_name):
        """Returns true if the enriched column looks interesting"""
        return False

    def enrich(self, column):
        """Expand the column into interesting parts."""
        # _start = datetime.now()
        assert self._detector is not None
        self.enriched_df = pd.DataFrame()
        return self.enriched_df


class FeatrixFieldTimeIntervalEnrichment(FeatrixFieldBaseEnrichment):
    def __init__(self, detector):
        super().__init__(detector=detector)

    def looks_interesting(self, enriched_name):
        """Returns true if the enriched column looks interesting"""
        dataCol = self.enriched_df[enriched_name]
        data = dataCol[dataCol.notnull()]

        dataLen = len(data)

        dataUniques = data.unique()
        dataUniquesLen = len(dataUniques)

        if dataUniquesLen == dataLen:
            return False

        try:
            entropy = SS.entropy(data.value_counts(), base=2)
            if entropy < 1:
                return False
        except Exception:
            # Catch entropy() crashes.
            traceback.print_exc()

        return True

    def enrich(self, column):
        """Expand the column into interesting parts."""
        assert self._detector is not None
        interval = self._detector.cast_values(column)
        assert interval is not None

        self.enriched_df[self.format_new_col_name("interval_seconds")] = interval

        # FIXME: could do more... days/hours.

        return self.enriched_df


class FeatrixFieldTimeEnrichment(FeatrixFieldBaseEnrichment):
    def __init__(self, detector):
        super().__init__(detector=detector)

    def looks_interesting(self, enriched_name):
        """Returns true if the enriched column looks interesting"""
        # all uniques? No
        # FIXME: we want some cross-entropy or predictive power assessment on these fields.
        # FIXME: this is pretty dumb.
        # print("looks_interesting on %s called" % enriched_name)
        dataCol = self.enriched_df[enriched_name]
        data = dataCol[dataCol.notnull()]

        dataLen = len(data)

        dataUniques = data.unique()
        dataUniquesLen = len(dataUniques)
        # if dataUniquesLen < 10:
        #    print("dataUniques = ", dataUniques)
        # print(f"{enriched_name} -- dataUniquesLen = {dataUniquesLen}; dataLen = {dataLen}")
        # print()

        if dataUniquesLen == dataLen:
            return False

        try:
            entropy = SS.entropy(data.value_counts(), base=2)
            # norm = entropy / float(dataLen)
            # print("norm entropy: ", entropy, norm)
            if entropy < 1:
                return False
        except Exception:
            # Catch entropy() crashes.
            traceback.print_exc()

        return True

    def enrich(self, column):
        """Expand the column into interesting parts."""
        assert self._detector is not None
        datetimeColumn = self._detector.cast_values(column)
        assert datetimeColumn is not None

        self.enriched_df[
            self.format_new_col_name("day_of_year")
        ] = datetimeColumn.dt.dayofyear.astype("float")
        self.enriched_df[
            self.format_new_col_name("day_of_month")
        ] = datetimeColumn.dt.day.astype("float")
        self.enriched_df[
            self.format_new_col_name("day_of_week")
        ] = datetimeColumn.dt.dayofweek.astype("float")
        self.enriched_df[
            self.format_new_col_name("hour_of_day")
        ] = datetimeColumn.dt.hour.astype("float")
        self.enriched_df[
            self.format_new_col_name("month")
        ] = datetimeColumn.dt.month.astype("float")

        self.enriched_df[
            self.format_new_col_name("year")
        ] = datetimeColumn.dt.year.astype('float')

        self.enriched_df[
            self.format_new_col_name("day_of_year")
        ] = datetimeColumn.dt.dayofyear.astype('float')

        try:
            self.enriched_df[
                self.format_new_col_name("week_of_year")
            ] = datetimeColumn.dt.isocalendar().week.astype('float')
        except:
            traceback.print_exc()
            pass

        return self.enriched_df


class FeatrixFieldFreeStringEnrichment(FeatrixFieldBaseEnrichment):
    def __init__(self, detector):
        super().__init__(detector=detector)
        self.enriched_df = pd.DataFrame()
        self._conversion_worked = False

    def looks_interesting(self, enriched_name):
        """Returns true if the enriched column looks interesting"""
        # all uniques? No
        # FIXME: we want some cross-entropy or predictive power assessment on these fields.
        # FIXME: this is pretty dumb.
        # print("enriched_name:", enriched_name)
        # dataCol = self.enriched_df[enriched_name]
        # data = dataCol[dataCol.notnull()]
        #
        # dataLen = len(data)
        #
        # dataUniques = list(data.unique())
        # dataUniquesLen = len(dataUniques)
        #
        # # is the type all numbers? mostly numbers?
        # # is the spacing non-uniform?
        # dataUniques.sort()
        #
        # # pick some samples -- what's the distance?
        # print("@@@ looks_interesting:", enriched_name)
        # uniques = self.enriched_df[enriched_name].unique()
        # vc = self.enriched_df[enriched_name].value_counts()
        # print("@@@ --> ", vc)
        return True

    def format_new_col_name(self, val):
        # FIXME: need to make 'val' a safe string for column names.
        # FIXME: ASCII, etc only characters... who knows what else.
        val = val.replace(" ", "_")
        val = val.replace(",", "_")
        val = val.replace(".", "_")
        val = val.replace("@", "_")
        return f"{self.get_col_name()}_featrix_free_string_mask_{val}"

    def enrich(self, column):
        # given the column, grab the value counts.
        # print("column = ", column)
        histogram = column.value_counts()

        h_num_entries = len(histogram)
        h_total = sum(histogram.to_dict().values())

        bit_field_max = min(5, h_num_entries / 4)

        d = histogram.nlargest(bit_field_max).to_dict()
        d_total = sum(d.values())

        if h_num_entries == 0:
            # print("got nuttin")
            return
        # print(d)
        normalized_weight = 1.0 / float(h_num_entries)
        # print("... d_total = ", d_total, "threshold = ", (2.0 * len(d) * normalized_weight))
        if d_total > (2.0 * len(d) * normalized_weight):
            # if 25% of the strings carry more than 50% of the instances, then
            # the distribution is lopsided -- and we might find utility in some bit fields
            # that carry whether the strings were specific values.
            # print("ITS BIG!", d_total)
            for d_key, _ in d.items():
                new_col = self.format_new_col_name(d_key)
                print("SETTING %s --> %s" % (new_col, d_key))
                self.enriched_df[new_col] = column[column == d_key]
                print(self.enriched_df[new_col].unique())
        # endif
        print(" --> self.enriched_df = ", self.enriched_df.columns)
        return self.enriched_df


class FeatrixFieldSetEnrichment(FeatrixFieldBaseEnrichment):
    def __init__(self, detector):
        super().__init__(detector=detector)
        self._conversion_worked = False

    def looks_interesting(self, enriched_name):
        """Returns true if the enriched column looks interesting"""
        # all uniques? No
        # FIXME: we want some cross-entropy or predictive power assessment on these fields.
        # FIXME: this is pretty dumb.
        # print("enriched_name:", enriched_name)
        dataCol = self.enriched_df[enriched_name]
        data = dataCol[dataCol.notnull()]  # .astype(dtype='float', errors='ignore')

        # dataLen = len(data)

        dataUniques = list(data.unique())
        dataUniquesLen = len(dataUniques)

        # is the type all numbers? mostly numbers?
        # is the spacing non-uniform?

        # for the below, we look for all numbers.

        # dataUniques
        #
        try:
            dataUniques.sort()
        except TypeError as err:
            numErrors = 0
            du = []
            for entry in dataUniques:
                try:
                    x = float(entry)
                    du.append(x)
                except:
                    numErrors += 1

            print("numErrors... = %s, len = %s" % (numErrors, dataUniquesLen))

            dataUniques = du
            dataUniquesLen = len(du)

            # Well, it's a mixed list... let's print it out.
            # print("crash - len(dataUniques) = ", len(dataUniques))
            # print(dataUniques)
            # import os
            # os._exit(2)
        if dataUniquesLen == 0:
            return True  # i guess...

        # pick some samples -- what's the distance?

        maxSamples = min(100, int(dataUniquesLen / 2) - 1)
        # print("maxSamples = ", maxSamples)
        if dataUniquesLen < 3 or maxSamples <= 3:
            return False  # just in case... seems sketchy

        for _ in range(0, maxSamples):
            idx = random.randint(1, dataUniquesLen - 2)
            if idx >= dataUniquesLen - 1:
                idx -= 1
            stuff = [dataUniques[idx - 1], dataUniques[idx], dataUniques[idx + 1]]
            ok_to_work = True
            for s in stuff:
                if s is None:
                    ok_to_work = False
                    break
                if type(s) == str:
                    ok_to_work = False

                try:
                    if math.isnan(s):
                        ok_to_work = False
                except:
                    pass

            if ok_to_work:
                di = abs(dataUniques[idx] - dataUniques[idx - 1])
                dj = abs(dataUniques[idx] - dataUniques[idx + 1])
                # print("idx search range:", idx - 1, idx, idx + 1, "; max range = ", dataUniquesLen - 1)
                if di != dj:
                    print("@@@", enriched_name, ": unequal range: ", di, dj, stuff)
                    return True

        return False

    def enrich(self, column):
        self._conversion_worked = False
        try:
            self.enriched_df[self.format_new_col_name("scalar")] = column.astype(
                "float", errors="ignore"
            )  # feeling risky....
            self._conversion_worked = True
        except:
            traceback.print_exc()
            self.enriched_df = pd.DataFrame()
        return self.enriched_df


EnrichMap = {
    FeatrixFieldTimeDetection.DETECTOR_NAME: FeatrixFieldTimeEnrichment,
    FeatrixFieldTimeIntervalDetection.DETECTOR_NAME: FeatrixFieldTimeIntervalEnrichment,
    FeatrixEmailDetection.DETECTOR_NAME: FeatrixFieldEmailEnrichment,
    # FeatrixFieldSetDetection.DETECTOR_NAME:   FeatrixFieldSetEnrichment,
    FeatrixDomainNameDetection.DETECTOR_NAME: FeatrixFieldDomainEnrichment,
}
