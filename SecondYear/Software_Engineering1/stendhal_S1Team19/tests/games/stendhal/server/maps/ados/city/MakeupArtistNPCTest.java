package games.stendhal.server.maps.ados.city;

import static org.junit.Assert.*;
import static utilities.SpeakerNPCTestHelper.getReply;

import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

import games.stendhal.server.core.engine.SingletonRepository;
import games.stendhal.server.core.engine.StendhalRPZone;
import games.stendhal.server.entity.item.Item;
import games.stendhal.server.entity.npc.SpeakerNPC;
import games.stendhal.server.entity.npc.fsm.Engine;
import games.stendhal.server.entity.player.Player;
import games.stendhal.server.maps.MockStendlRPWorld;
import utilities.PlayerTestHelper;
import utilities.RPClass.ItemTestHelper;

public class MakeupArtistNPCTest {

	private static Player player = null;
	private SpeakerNPC npc = null;
	private Engine en = null;

	@BeforeClass
	public static void setUpBeforeClass() throws Exception {

		final StendhalRPZone zone = new StendhalRPZone("admin_test");
		MockStendlRPWorld.get().addRPZone(new StendhalRPZone("0_ados_city_n"));
		new MakeupArtistNPC().configureZone(zone, null);

		player = PlayerTestHelper.createPlayerWithOutFit("player");

		zone.add(player);
		player.setPosition(19, 12);

	}

	@AfterClass
	public static void afterClass() {
		PlayerTestHelper.removePlayer(player);
	}

	@Test
	public void testMasks() {
		
		npc = SingletonRepository.getNPCList().get("Fidorea");
		Engine en = npc.getEngine();
		en = npc.getEngine();
		Item item = ItemTestHelper.createItem("money", 20);
		player.getSlot("bag").add(item);
		//Test you can buy a mask and she offers all masks
		en.step(player, "hello");
		assertEquals("Hi, there. Do you need #help with anything?", getReply(npc));
		en.step(player, "help");
		assertEquals("I sell masks, would you like to see what I #offer. If you don't like your mask, you can #return and I will remove it, or you can just wait 5 hours, until it wears off.", getReply(npc));
		en.step(player, "offer");
		assertEquals("You can #buy mouse mask, dog mask, monkey mask, penguin mask, cat mask, and frog mask.", getReply(npc));
	    en.step(player, "buy mouse mask");
		assertEquals("To buy a mouse mask will cost 20. Do you want to buy it?", getReply(npc));
		en.step(player, "yes");
		assertEquals("Thanks, and please don't forget to #return it when you don't need it anymore!", getReply(npc));
		//Test you can return the mask
		en.step(player, "return");
		assertEquals("Thank you!", getReply(npc));
		en.step(player, "goodbye");
		//Test you can't buy mask with insufficient funds
		en.step(player, "hello");
		assertEquals("Hi, there. Do you need #help with anything?", getReply(npc));
		en.step(player, "help");
		assertEquals("I sell masks, would you like to see what I #offer. If you don't like your mask, you can #return and I will remove it, or you can just wait 5 hours, until it wears off.", getReply(npc));
		en.step(player, "offer");
		assertEquals("You can #buy mouse mask, dog mask, monkey mask, penguin mask, cat mask, and frog mask.", getReply(npc));
	    en.step(player, "buy mouse mask");
		assertEquals("To buy a mouse mask will cost 20. Do you want to buy it?", getReply(npc));
		en.step(player, "yes");
		assertEquals("Sorry, you don't have enough money!", getReply(npc));

	}
}
