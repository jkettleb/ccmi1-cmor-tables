#!/usr/bin/env python

class MipTable(object):
    _IGNORE_VARS = 'orog p0 ptop a b a_bnds b_bnds ap ap_bnds ztop'.split()
    
    def __init__(self, table):
        self.table = table
        self.name = os.path.basename(table)
        self._vars = self._parse_for_vars() # only needed once

    def vars(self):
        return self._vars
    
    def _parse_for_vars(self):
        with open(self.table, 'r') as fi:
            result = [self._parse_line(line) \
                      for line in fi.readlines() \
                      if self._non_dim_variable(line)]
        return result

    def _non_dim_variable(self, line):
        return line.startswith('variable_entry') and \
          self._parse_line(line) not in self._IGNORE_VARS
    
    def _parse_line(self, line):
        return line[15:].strip()
    
import os
class MipProject(object):
    def __init__(self, mip_dir):
        self.mip_dir = mip_dir
        self.tables = self._tables() #only needed once
        
    def tables_containing_var(self, var):
        return [table.name \
                for table in self.tables \
                if var in table.vars()]
                
    def _tables(self):
        return [MipTable(os.path.join(self.mip_dir, table)) \
                for table in os.listdir(self.mip_dir)]

def results_for_table(table, project):
    print '***' + table.name + '***'
    for var in table.vars():
        print var, project.tables_containing_var(var)
    print '\n\n'

def main():
    project = MipProject('/project/ipcc/ar5/etc/mip_tables/CMIP5/20130717')

    for table in MipProject('./Tables').tables:
        results_for_table(table, project)
        
if __name__ == '__main__':
    main()
