////////////////////////////////////////////////////////////
// This is an example contract hacked together at a meetup.
// It is by far not complete and only used to show some
// features of Solidity.
////////////////////////////////////////////////////////////
pragma solidity ^0.4.25;
import "github.com/ethereum/dapp-bin/library/pqueue.sol";
//import "pqueue.sol";

contract Auction is queue {
    //data
    Queue buyerList;
    Queue sellerList;
    bool matchingSuccess;
    
    mapping (address => uint ) public havePowerAmount;
    
    //function
    constructor() public {
        buyerList.trades.length = 200;
        sellerList.trades.length = 200;
        setSort(buyerList, true);
        setSort(sellerList, false);
        matchingSuccess = false;
    }
    
    //buyer
    function addRequest_buy(uint powerAmount) payable public {
        if(msg.sender.balance > msg.value)
            push(buyerList, msg.sender, powerAmount, msg.value);
    }
    
    function queueSize_buy() public view returns (uint) {
        return size(buyerList);
    }
    function queueTop_buy() public view returns (uint){
        return top_kwPerPrice(buyerList);
    }
    
    //seller
    function addRequest_sell(uint powerAmount, uint d) public {
        //havePowerAmount[msg.sender] -= powerAmount;
        push(sellerList, msg.sender, powerAmount, d);
    }
    
    function queueSize_sell() public view returns (uint) {
        return size(sellerList);
    }
    function queueTop_sell() public view returns (uint){
        return top_kwPerPrice(sellerList);
    }
    
    //matching
    function matchingCheck() public view returns (bool){
        return matchingSuccess;
    }
    
    function matching() public payable {
        matchingSuccess = false;
        uint sellerPrice = top_kwPerPrice(sellerList);
        uint buyerPrice = top_kwPerPrice(buyerList);
        if(buyerPrice > sellerPrice){
            Trade memory seller;
            Trade memory buyer;
            seller.addr = top_addr(sellerList);
            seller.powerAmount = top_powerAmount(sellerList);
            seller.fee = top(sellerList);
            seller.kwPerPrice = top_kwPerPrice(sellerList);
            
            buyer.addr = top_addr(buyerList);
            buyer.powerAmount = top_powerAmount(buyerList);
            buyer.fee = top(buyerList);
            buyer.kwPerPrice = top_kwPerPrice(buyerList);

            pop(sellerList);
            pop(buyerList);
            
            if(seller.powerAmount > buyer.powerAmount){
                havePowerAmount[buyer.addr] += buyer.powerAmount;
                //havePowerAmount[seller.addr] -= buyer.powerAmount;
                seller.powerAmount -= buyer.powerAmount; 
                seller.fee = seller.powerAmount * seller.kwPerPrice;
                
                seller.addr.transfer(buyer.fee);
                push(sellerList, seller.addr, seller.powerAmount, seller.fee);
                matchingSuccess = true;
                return;
                
            }else if (seller.powerAmount < buyer.powerAmount){
                havePowerAmount[buyer.addr] += seller.powerAmount;
                //havePowerAmount[seller.addr] -= seller.powerAmount;
                buyer.powerAmount -= seller.powerAmount;
                uint sendFee = seller.powerAmount * buyer.kwPerPrice;
                buyer.fee = buyer.fee - sendFee;
                
                seller.addr.transfer(sendFee);
                push(buyerList, buyer.addr, buyer.powerAmount, buyer.fee);
                matchingSuccess = true;
                return;
                
            }else if(seller.powerAmount == buyer.powerAmount){
                havePowerAmount[buyer.addr] += buyer.powerAmount;
                //havePowerAmount[seller.addr] -= buyer.powerAmount;
                
                seller.addr.transfer(buyer.fee);
                matchingSuccess = true;
                return;
            }
            matchingSuccess = false;
            return;
        }
        matchingSuccess = false;
        return;
    }
    
}
