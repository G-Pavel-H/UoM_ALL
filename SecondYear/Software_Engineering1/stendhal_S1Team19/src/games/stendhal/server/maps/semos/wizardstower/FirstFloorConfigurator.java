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
package games.stendhal.server.maps.semos.wizardstower;

import java.util.Map;

import games.stendhal.server.core.config.ZoneConfigurator;
import games.stendhal.server.core.engine.StendhalRPZone;
import games.stendhal.server.core.events.ItemDropListener;
import games.stendhal.server.entity.item.Item;
import games.stendhal.server.entity.player.Player;
import marauroa.common.game.RPAction;

public class FirstFloorConfigurator implements ZoneConfigurator, ItemDropListener{
	/**
	 * Configure a zone.
	 *
	 * @param	zone		The zone to be configured.
	 * @param	attributes	Configuration attributes.
	 */

	@Override
	public void configureZone(final StendhalRPZone zone, final Map<String, String> attributes) {
        zone.addItemDropListener(this);
	}

    @Override
    public boolean onDrop(Item item, StendhalRPZone zone, RPAction action, Player player) {
        // can't drop candles here to prevent 
	    //System.out.println("RUNNING HEREEE");
       // return true;
        return !(item.getName().equals("candle") && player != null);
    }
}