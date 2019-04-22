#!/usr/bin/python3.6
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_get
from nornir.plugins.functions.text import print_result
from nornir.core.filter import F
import ipdb

def get_facts_manually(task):
    #ipdb.set_trace(context=5)
    task.host.open_connection("napalm", configuration=task.nornir.config)
    r = task.run(napalm_get, getters=['facts'])
    task.host.close_connection("napalm")

if __name__ == "__main__":
    norn = InitNornir(config_file='config.yaml')

    #devs = norn.filter(hostname='r1')
    #devs = norn.filter(F(groups__contains='Switches'))
    devs = norn.filter(F(groups__contains='Routers'))
    facts = devs.run(task=get_facts_manually)
    print_result(facts)
