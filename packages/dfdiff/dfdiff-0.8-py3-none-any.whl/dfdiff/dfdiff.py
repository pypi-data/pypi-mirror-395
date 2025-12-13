import pandas as pd
import numpy as np

import sys

def pdprint(pdobj):
    with pd.option_context('display.max_rows', None, 'display.max_columns', 
            None, 'display.max_seq_items', None):
        print(pdobj)


class dfdiff():
    def __init__(self, l, r, key):
        self.key = key
        self.l = l
        self.r = r

        # gather metadata information about the columns/fields
        # from both files
        self.lcol = self._getColDf(self.l, "l")
        self.rcol = self._getColDf(self.r, "r")
        
        self.fdiff = self.lcol.merge(self.rcol, how='outer', left_on=['l_fname'],
                right_on=['r_fname'], indicator=True)
        self.inlnotr = self.fdiff[self.fdiff['_merge']=="left_only"]['l_fname'].tolist()
        self.inrnotl = self.fdiff[self.fdiff['_merge']=="right_only"]['r_fname'].tolist()
        self.scol = self.fdiff[self.fdiff['_merge']=="both"]['l_fname'].tolist()
        self.fdiff = self.fdiff[['l_ordinalposition', 'l_fname','r_fname','r_ordinalposition','_merge']].sort_values(by='r_ordinalposition')

        # strip and apply standardized changes to all fields
        # from both files
        self.l[self.l.columns] = self._procCols(self.l)
        self.r[self.r.columns] = self._procCols(self.r)


        # validate the key is in list of shared columns
        err = []
        lcolls = self.lcol['l_fname'].to_list()
        rcolls = self.rcol['r_fname'].to_list()
        for k in self.key:
            if k not in lcolls or k not in rcolls:
                err.append(k)
        if err:
            print(f"*** columns {err} are not part of the shared columns\n"+
                  f"    between the left and right dataset shared columns\n"+
                  f"{self.scol}", file=sys.stderr)
            sys.exit(1)

        # validate the uniqueness of the primary key to be
        # used for testing, display warning if the key is not unique
        # in either the left or right table, implies not a true
        # 1:1 join

        self.dupkey = self._testUniqueness(self.l, "L")
        self.dupkey = pd.concat([self.dupkey, self._testUniqueness(self.r, "R")])

        self.m = self.l.merge(self.r, how='outer', on=self.key, 
                         suffixes=('_l','_r'), indicator=True
                )
        self.celldiffdf = None
        self.recdiffdf = None
        self.celldiffdf = self.getCellDiffDf()
        self.recdiffdf = self.getRecDiffDf()

    def _getColDf(self, df, side):
        ret = pd.DataFrame(df.columns.to_list(), columns=[f"{side}_fname"])
        ret = ret.reset_index()
        ret = ret.rename({'index':f"{side}_ordinalposition"}, axis=1)
        ret[f"{side}_ordinalposition"] = pd.to_numeric(ret[f"{side}_ordinalposition"], downcast="integer")
        return ret

    def _testUniqueness(self, data, side):
        s = data.groupby(self.key).size()
        s = s[s>1]
        if s.size > 0:
            ret = pd.DataFrame(data=s, index=s.index, dtype=str,
                columns=['count']).reset_index()
            ret['exists'] = side
            return ret
        else:
            # if no duplicate create empty dataframe for this
            ret = pd.DataFrame(data=[], dtype=str, 
                columns=self.key+['count','exists'])
            return ret

    def getDiffDfs(self):
        return self.fdiff, self.celldiffdf, self.recdiffdf, self.dupkey

    def _procCols(self, df):
        ret = df.copy()
        ret[ret.columns] = ret.apply(lambda c: c.fillna(""))
        ret[ret.columns] = ret.apply(lambda c: c.str.strip())
        return ret

    def printDiff(self):
        for c in self.scol:
            coldiff = self.diffdf[self.diffdf['fname']==c]
            if coldiff.shape[0] != 0:
                print(f"Difference found in '{c}' Field")
                print(f"{coldiff}\n")

    def getFieldDiffList(self):
        return self.celldiffdf['fname'].unique().tolist()

    def getRecDiffDf(self):
        if self.recdiffdf is None:
            left = self.m[self.m['_merge']=='left_only'][self.key].copy()
            left['exists'] = "L"
            right = self.m[self.m['_merge']=='right_only'][self.key].copy()
            right['exists'] = "R"
            recdiffdf = pd.concat([left,right])
            return recdiffdf
        else:
            return self.recdiffdf

    def getCellDiffDf(self):
        if self.celldiffdf is None:
            celldiffdf = None
            for c in self.scol:
                # if column is part of the primary key it need to be
                # skipped
                if c in self.key:
                    continue

                # if column is not part of the primary key, continue
                # to analyze column difference
                cols = [f"{c}_l", f"{c}_r"]
                diffdata = ['fname','lval','rval']
                datadiffdf = self.m[(self.m[cols[0]] != self.m[cols[1]]) &
                                    (self.m['_merge']=="both")]
                if datadiffdf.shape[0] != 0:
                    mapper = dict(zip(cols,['lval','rval']))
                    datadiffdf = datadiffdf.rename(columns=mapper)
                    datadiffdf['fname'] = c
                    datadiff = datadiffdf[self.key+diffdata].copy()
                    if celldiffdf is None:
                        celldiffdf = datadiff
                    else:
                        celldiffdf = pd.concat([celldiffdf, datadiff],
                                ignore_index=True)

            # if there is absolutely no data difference found,
            # create an empty dataframe
            if celldiffdf is None:
                celldiffdf = pd.DataFrame(
                        columns=self.key+diffdata,
                        dtype=str)
            return celldiffdf
        else:
            return self.celldiffdf

    def __repr__(self):
        return f"""\
Field in l not r: {self.inlnotr}
Field in r not l: {self.inrnotl}
Field where differences are observed: {self.getFieldDiffList()}
"""
