#!/usr/bin/env python

from StringIO import StringIO
from zipfile import ZipFile
from urllib import urlopen
import shutil
import os

formulas = {}

# Key   = github URL name to formula; ie: https://github.com/${org}/${key}/archive/master.zip
# Value/List = directory/name of formulas within repo (these get copied to salt states root, and is therefore the name referenced in top.sls)

formulas["vault-formula"] = ["vault"]
formulas["nomad-formula"] = ["nomad"]

if __name__ == "__main__":
    for formula in formulas:
        print "processing {0}".format(formula)
        print "downloading https://github.com/saltstack-formulas/{0}/archive/master.zip".format(formula)
        resp = urlopen('https://github.com/saltstack-formulas/{0}/archive/master.zip'.format(formula))
        zipfile = ZipFile(StringIO(resp.read()))
        if os.path.exists('salt/states/{0}'.format(formula)):
            print "deleting existing salt/states/{0}".format(formula)
            shutil.rmtree('salt/states/{0}'.format(formula))
        zipfile.extractall("salt/states/{0}".format(formula))
        for state in formulas[formula]:
            if os.path.exists('salt/states/{0}'.format(state)):
                print "deleting existing salt/states/{0}".format(state)
                shutil.rmtree('salt/states/{0}'.format(state))
            print "moving salt/states/{0}/{1}-master/{2} -> salt/states/{3}".format(formula,formula,state,state)
            shutil.move("salt/states/{0}/{1}-master/{2}".format(formula,formula,state), "salt/states/")
        print "deleting salt/states/{0}".format(formula)
        shutil.rmtree('salt/states/{0}'.format(formula))