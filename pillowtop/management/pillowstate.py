import simplejson
from corehq.elastic import get_es
from pillowtop.listener import AliasedElasticPillow


def get_pillow_states(pillows):
    """
    Return states of all pillows

    mapped_masters: current indices that are correctly aliased
    unmapped_masters: current indices that are not yet aliased
    stale_indices: indices that are not master but may or may not have an active alias
    """
    es = get_es()
    system_status = es.get('_status')

    aliased_pillows = filter(lambda x: isinstance(x, AliasedElasticPillow), pillows)
    master_aliases = dict((x.es_index, x.es_alias) for x in aliased_pillows)

    #all live indices on ES
    active_indices = system_status['indices'].keys()
    active_aliases = es.get('_aliases')

    def has_alias(target_alias, alias_dict):
        return target_alias in alias_dict

    #check if masters are ok
    nonexistent_masters = set(master_aliases.keys()) - set(active_indices)
    active_master_indices = set(master_aliases.keys()).intersection(active_indices)
    active_masters = set()
    inactive_masters = set()

    for am in active_master_indices:
        target_alias = master_aliases[am]
        if has_alias(target_alias, active_aliases.get(am, {}).get('aliases', {})):
            active_masters.add(am)
        else:
            inactive_masters.add(am)

    stale_indices = []
    non_master_indices = set(active_indices) - set(master_aliases.keys())
    for nm in non_master_indices:
        aliases_for_nm = active_aliases.get(nm, {}).get('aliases', {}).keys()
        stale_indices.append((nm, aliases_for_nm))

    mapped_masters = [(x, master_aliases[x]) for x in active_masters]
    unmapped_masters = [(x, master_aliases[x]) for x in inactive_masters.union(nonexistent_masters)]

    return mapped_masters, unmapped_masters, stale_indices
