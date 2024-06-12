package games.stendhal.server.maps.ados.market;

import static org.hamcrest.CoreMatchers.is;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertThat;
import org.junit.BeforeClass;
import org.junit.Test;
import games.stendhal.server.core.engine.SingletonRepository;
import games.stendhal.server.core.engine.StendhalRPZone;
import games.stendhal.server.entity.npc.NPC;
import games.stendhal.server.maps.MockStendlRPWorld;
import marauroa.common.Log4J;

public class FishSoupMakerNPCTest {

	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
		Log4J.init();
		MockStendlRPWorld.get();

	}

	/**
	 * Tests for configureZone.
	 */
	@Test
	public void testConfigureZone() {

		SingletonRepository.getRPWorld();
		final FishSoupMakerNPC fishSoupMakerConfigurator = new FishSoupMakerNPC();

		final StendhalRPZone zone = new StendhalRPZone("testzone");
		fishSoupMakerConfigurator.configureZone(zone, null);
		assertFalse(zone.getNPCList().isEmpty());
		final NPC fishSoupMaker = zone.getNPCList().get(0);
		assertEquals(fishSoupMaker.getName(), "Florence Bouillabaisse");
		assertThat(fishSoupMaker.getDescription(), is("You see Florence Bouillabaisse. She is an excellent soup chef."));
	}



}
