/* $Id$ */
/***************************************************************************
 *                   (C) Copyright 2003-2010 - Stendhal                    *
 ***************************************************************************
 ***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
package games.stendhal.server.core.events;

import games.stendhal.server.core.engine.StendhalRPZone;
import games.stendhal.server.entity.item.Item;
import games.stendhal.server.entity.player.Player;
import marauroa.common.game.RPAction;

public interface ItemDropListener {
	/**
	 * Invoked when an item is dropped in a zone
	 *
	 * @param item
	 *            Item being dropped.
	 * @param zone
	 *            The new zone.
	 * @param player
	 * 			  The player dropping the item.
	 * 
	 * @return whether the item is allowed to be dropped in this zone.
	 * 			  
	 */
	boolean onDrop(Item item, StendhalRPZone zone, RPAction action, Player player);

}
