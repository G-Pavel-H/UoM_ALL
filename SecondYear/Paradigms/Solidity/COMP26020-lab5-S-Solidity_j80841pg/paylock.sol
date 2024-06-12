pragma solidity >=0.4.16 <0.7.0;

contract Paylock {
    
    enum State { Working , Completed , Done_1 , Delay , Done_2 , Forfeit }
    
    int disc;
    State st;
    int clock;
    address public timeAdd;
    
    constructor(address _timeAdd) public {
        st = State.Working;
        disc = 0;
        clock = 0;
        timeAdd = _timeAdd;
    }

    modifier onlyTimeAdd {
        require(msg.sender == timeAdd, "Only the timeAdd can call this function.");
        _;
    }
    
    function tick() external onlyTimeAdd {
        clock++;
    }

    function signal() public {
        require( st == State.Working );
        st = State.Completed;
        disc = 10;
    }

    function collect_1_Y() public {
        require( st == State.Completed && clock < 4 );
        st = State.Done_1;
        disc = 10;
    }

    function collect_1_N() external {
        require( st == State.Completed && clock >= 4 );
        st = State.Delay;
        disc = 5;
    }

    function collect_2_Y() external {
        require( st == State.Delay && clock >= 8 );
        st = State.Done_2;
        disc = 5;
    }

    function collect_2_N() external {
        require( st == State.Delay && clock < 8 );
        st = State.Forfeit;
        disc = 0;
    }

}
contract Supplier {
    
    Paylock p;
    Rental r;

    enum State { Working , Completed }
    
    State st;
    
    constructor(address pp, address payable rr) public {
        p = Paylock(pp);
        r = Rental(rr);
        st = State.Working;
    }

    function aquire_resource() payable public {
        require (st == State.Working && msg.value == 1 wei);
        r.rent_out_resource.value(1 wei)();
    }

    function return_resource() public {
        require (st == State.Working);
        r.retrieve_resource();
    }

    function finish() external {
        require (st == State.Working);
        p.signal();
        st = State.Completed;
    }
    
    receive() external payable {}
}

contract Rental {
    
    address payable resource_owner;
    bool resource_available;
    uint256 public constant depositAmount = 1 wei;
    
    constructor() public {
        resource_available = true;
    }
    
    function rent_out_resource() payable external {
        require(resource_available == true && msg.value == depositAmount, "Invalid amount");
        resource_owner = msg.sender;
        resource_available = false;
    }

    function retrieve_resource() external {
        require(resource_available == false && msg.sender == resource_owner);
        (bool success,) = resource_owner.call.value(depositAmount)("");
        require(success, "Return transfer failed");
        resource_available = true;
    }
    
}


