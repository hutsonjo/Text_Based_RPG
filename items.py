from UI import Item

health_potion = Item(
    "Health Potion",
    "A vial of red liquid that smells of yarrow flowers.\n\n-Restores 10 health-",
    True,
    apply_effect=lambda p: p.stats.update({"health": p.stats["health"] + 10})
)

old_broadsword = Item(
    "Old Broadsword",
    "A sword with a sturdy hilt and wide blade. It is covered in rust.\n\n-Adds 5 Attack while held-",
    False,
    equip_effect=lambda p: p.stats.update({"attack": p.stats["attack"] + 5}),
    remove_effect=lambda p: p.stats.update({"attack": p.stats["attack"] - 5})
)

ITEM_LOG = {'health_potion': health_potion,
            'old_broadsword': old_broadsword}
