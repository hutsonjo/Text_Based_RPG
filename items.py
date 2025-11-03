from UI import Item

health_potion = Item(
    "Health Potion",
    "A vial of red liquid that smells of yarrow flowers",
    "Restores 10 HP",
    apply_effect=lambda p: p.stats.update({"health": p.stats["health"] + 10})
)

old_broadsword = Item(
    "Old Broadsword",
    "A sword with a sturdy hilt and wide blade. It is covered in rust.",
    "Adds +5 Attack Value",
    apply_effect=lambda p: p.stats.update({"attack": p.stats["attack"] + 5}),
    remove_effect=lambda p: p.stats.update({"attack": p.stats["attack"] - 5})
)

