class ResourceValues:
    capacity: int
    wear_per_day: int  # bytes / day ?
    read_ops: int
    read_bandwidth: int
    write_ops: int
    write_bandwidth: int


class Storage:
    id: int
    is_working: bool
    # caractéristiques ? emplacement du stockage ? -> important mais plus tard
    resource_limits: ResourceValues
    resource_current: ResourceValues
    # threshold ? on verra ça plus tard


class Instances:
    id_vol: int  # id du volume ?
    vol_version: int  # ???
    local_id: int  # id
    bytes_used: int  # espace utilisé par l'objet dans cette instance


class Object:
    id: int
    instances_used: list[Instances]  # ensemble d'instances utilisées pour l'objet
    # état à définir ? + rajouter les SloSet
    is_sync: bool


class Proposal:
    original_object: Object  # objet avant modif (avec son instance)
    proposed_object: Object  # objet après modif
    proposal_type: str  # UNK, ADD, MOV, DEL
    gain: int  # gain estimé par notre truc ?
