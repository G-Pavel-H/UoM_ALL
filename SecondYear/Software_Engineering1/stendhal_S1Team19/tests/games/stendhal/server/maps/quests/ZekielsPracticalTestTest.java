package games.stendhal.server.maps.quests;

import org.junit.Test;
import org.xml.sax.SAXException;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

import games.stendhal.common.EquipActionConsts;
import games.stendhal.server.actions.equip.DropAction;
import games.stendhal.server.actions.equip.EquipmentAction;
import games.stendhal.server.core.engine.SingletonRepository;
import games.stendhal.server.core.engine.StendhalRPWorld;
import games.stendhal.server.core.engine.StendhalRPZone;
import games.stendhal.server.entity.item.Item;
import games.stendhal.server.entity.player.Player;
import marauroa.common.game.RPAction;
import games.stendhal.server.core.config.ZonesXMLLoader;

import utilities.PlayerTestHelper;

public class ZekielsPracticalTestTest {

	/**
	 * Tests for dropItem.
	 * @throws URISyntaxException
	 * @throws IOException
	 * @throws SAXException
	 */
	
	private StendhalRPWorld world;
	private String candle = "candle";

	public ZekielsPracticalTestTest() throws URISyntaxException, SAXException, IOException{
		ZonesXMLLoader loader = new ZonesXMLLoader(new URI("testsemos.xml"));
		loader.load();
		world = SingletonRepository.getRPWorld();
	}

	@Test
	public void testDropTower1() {
		StendhalRPZone zone = world.getZone("int_semos_wizards_tower_1");
		Player player = PlayerTestHelper.createPlayer("bob");
		player.setPosition(8, 16);
		Item item = SingletonRepository.getEntityManager().getItem(candle);

		player.equip("bag", item);
		assertTrue(player.isEquipped(candle));
		zone.add(player);
		RPAction drop = new RPAction();
		drop.put("type", "drop");
		drop.put("baseobject", player.getID().getObjectID());
		drop.put("baseslot", "bag");
		drop.put("x", player.getX());
		drop.put("y", player.getY() + 1);
		drop.put("quantity", "1");
		drop.put("baseitem", item.getID().getObjectID());

		final EquipmentAction action = new DropAction();
		assertEquals(0, zone.getItemsOnGround().size());
		assertTrue(drop.has(EquipActionConsts.BASE_ITEM));

		action.onAction(player, drop);
		assertEquals(0, zone.getItemsOnGround().size());
		assertTrue(player.isEquipped(candle));
	}
	
	@Test
	public void testDropOutside(){
		StendhalRPZone zone = world.getZone("0_semos_mountain_n_w4");
		Player player = PlayerTestHelper.createPlayer("sam");
		Item item = SingletonRepository.getEntityManager().getItem(candle);

		player.equip("bag", item);
		assertTrue(player.isEquipped(candle));
		zone.add(player);
		RPAction drop = new RPAction();
		drop.put("type", "drop");
		drop.put("baseobject", player.getID().getObjectID());
		drop.put("baseslot", "bag");
		drop.put("x", player.getX());
		drop.put("y", player.getY() + 1);
		drop.put("quantity", "1");
		drop.put("baseitem", item.getID().getObjectID());

		final EquipmentAction action = new DropAction();
		assertEquals(0, zone.getItemsOnGround().size());
		assertTrue(drop.has(EquipActionConsts.BASE_ITEM));

		action.onAction(player, drop);
		assertEquals(1, zone.getItemsOnGround().size());
		assertFalse(player.isEquipped(candle));	
	}
	
}