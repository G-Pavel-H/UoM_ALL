/***************************************************************************
 *                   (C) Copyright 2015 - Faiumoni e. V.                   *
 ***************************************************************************
 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
package games.stendhal.server.entity.item;

import java.util.Map;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

import games.stendhal.server.entity.Outfit;
import games.stendhal.server.entity.RPEntity;
import games.stendhal.server.entity.player.Player;
import marauroa.common.game.SlotOwner;

import org.apache.log4j.Logger;

/**
 * an item that disguises you from selected hostile creatures
 */
public class Disguise extends Item {
	private static final Logger logger = Logger.getLogger(Disguise.class);

	/**
	 * copy constructor
	 *
	 * @param item item to copy
	 */
	public Disguise(Disguise item) {
		super(item);
	}		// for disguises
	

	private List<String> slots = (Arrays.asList("armor", "feet", "head", "legs"));

	/**
	 * creates a new item
	 *
	 * @param name item name
	 * @param clazz item class
	 * @param subclass item subclass
	 * @param attributes attributes
	 */
	public Disguise(String name, String clazz, String subclass, Map<String, String> attributes) {
		super(name, clazz, subclass, attributes);
	}

	private Player owner;

	@Override
	public boolean onEquipped(RPEntity equipper, String slot) {
		if (slots.contains(slot)){
			if (equipper instanceof Player) {
				logger.error("Disguise onEquipped called" + this.getDisguisedTo());
				Player player = (Player) equipper;
				owner = player;
				Outfit outfit = player.getOutfit();
				outfit.setLayer("disguise", Integer.parseInt(get("disguise_id")));
				player.setOutfit(outfit);
				logger.error(outfit);
				List<String> currentDisguised = player.getDisguisedTo();
				currentDisguised.addAll(this.getDisguisedTo());
				player.setDisguisedTo(currentDisguised);
			}
		}
		return super.onEquipped(equipper, slot);
	}

	@Override
	public boolean onUnequipped() {
		SlotOwner equipper = this.getContainerOwner();
		if (equipper instanceof Player) {
			final String slot = getContainerSlot().getName();
			if (slots.contains(slot)){
				logger.error("Disguise onUnEquipped called" + this.getDisguisedTo());
				Player player = (Player) equipper;
				owner = player;
				Outfit outfit = player.getOutfit();
				outfit.setLayer("disguise", 0);
				player.setOutfit(outfit);
				List<String> currentDisguised = player.getDisguisedTo();
				for (String i : this.getDisguisedTo()){
					currentDisguised.remove(i);
				}
				player.setDisguisedTo(currentDisguised);

			}
		}
		return super.onUnequipped();
	}


}
