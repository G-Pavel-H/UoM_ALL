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
package games.stendhal.server.entity.player;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.BeforeClass;
import org.junit.Test;

import games.stendhal.server.core.engine.StendhalRPZone;
import games.stendhal.server.entity.creature.Sheep;
import games.stendhal.server.maps.MockStendlRPWorld;
import marauroa.common.Log4J;
import utilities.PlayerTestHelper;
import utilities.RPClass.PetTestHelper;
import utilities.RPClass.SheepTestHelper;

public class PetTest {

	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
		Log4J.init();
		assertTrue(MockStendlRPWorld.get() instanceof MockStendlRPWorld);
		PlayerTestHelper.generateCreatureRPClasses();
		PetTestHelper.generateRPClasses();
		SheepTestHelper.generateRPClasses();
	}

	/**
	 * Tests for pet preventing player movement between zones.
	 */
	@Test
	public void testPetPlayerZoneChange() { //double check, this may need to be in a different file
		final StendhalRPZone zone = new StendhalRPZone("testzone", 100, 100);
		MockStendlRPWorld.get().addRPZone(zone);
		final Player bob = PlayerTestHelper.createPlayer("bob");
		zone.add(bob);
		final Sheep meh = new Sheep(bob);
		zone.add(meh);
		
		bob.setIgnoresCollision(false);
		
		bob.teleport(zone,0,0,null,bob);//teleport bob to the edge of the map
		
		assertTrue(zone.leavesZone(bob,-1,-1));
		
		// TRIGGER handleSimpleCollision in Player.java indirectly 
		
		meh.setPosition(0,0); //teleport pet next to bob
		assertTrue(bob.isZoneChangeAllowed());
		bob.handleSimpleCollision(-1, -1);
		assertTrue(bob.events().isEmpty()); //assert that bob has not received a message
		
		meh.setPosition(100,100); //teleport pet too far away to leave zone
		assertFalse(bob.isZoneChangeAllowed());
		bob.handleSimpleCollision(-1, -1);
		assertFalse(bob.events().isEmpty()); //asserts that bob has received message to say pet is too far away
	}
}
