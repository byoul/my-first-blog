pragma solidity ^0.4.25;

contract queue
{
    struct Queue {
        Trade[] trades;
        uint front;
        uint back;
        bool sort;//true : MaxHeap, false : MinHeap
    }
    struct Trade{
        address addr;
        uint powerAmount;
        uint fee;
        uint kwPerPrice;
    }
    function setSort(Queue storage q, bool sort) internal {
        q.sort = sort;
    }
    
    function comp(Queue storage q, uint a, uint b) constant internal returns (bool){
        if(q.sort){
            if(a>b) return true;
            else return false;
        }
        else{
            if(a<b) return true;
            else return false;
        }
    }
    function getFront(Queue storage q) constant internal returns (uint){
        return q.front;
    }
    function getBack(Queue storage q) constant internal returns (uint){
        return q.back;
    }
    
    function empty(Queue storage q) constant internal returns (bool){
        if( q.back - q.front ==0) return true;
        else return false;
    }
    
    function size(Queue storage q) constant internal returns (uint) {
        return q.back - q.front;
    }
    function top(Queue storage q) constant internal returns (uint) {
        return q.trades[q.front].fee;
    }
    function top_addr(Queue storage q) constant internal returns (address) {
        return q.trades[q.front].addr;
    }
    function top_powerAmount(Queue storage q) constant internal returns (uint) {
        return q.trades[q.front].powerAmount;
    }
    function top_kwPerPrice(Queue storage q) constant internal returns(uint){
        return q.trades[q.front].kwPerPrice;
    }

    function capacity(Queue storage q) constant internal returns (uint) {
        return q.trades.length - 1;
    }
    
    function push(Queue storage q, address addr, uint powerAmount, uint data) internal
    {
        if ((q.back + 1) % q.trades.length == q.front)
            return; // throw;
        
        uint idx = q.back;
        
        q.trades[idx].addr = addr;
        q.trades[idx].powerAmount = powerAmount;
        q.trades[idx].fee = data;
        q.trades[idx].kwPerPrice = data / powerAmount;
        
        q.back = (q.back + 1) % q.trades.length;
        
        while(idx > q.front){
            if(comp(q, q.trades[idx].kwPerPrice, q.trades[idx/2].kwPerPrice)){
                Trade memory tmp = q.trades[idx];
                q.trades[idx] = q.trades[idx/2];
                q.trades[idx/2] = tmp;
                
                idx = idx/2;
                
            }
            
            else break;
        }
    }
    
    function pop(Queue storage q) internal returns (address addr, uint powerAmount, uint fee, uint KwPerPrice)
    {
        if(q.back - q.front == 0 ) return;
        addr = q.trades[q.front].addr;
        powerAmount = q.trades[q.front].powerAmount;
        fee = q.trades[q.front].fee;
        KwPerPrice = q.trades[q.front].kwPerPrice;
        q.back = (q.back-1) % q.trades.length;
        
        q.trades[q.front] = q.trades[q.back];
        delete q.trades[q.back];

        uint idx = q.front;
        while(idx < q.back-1){
            uint cmpIdx;
            if(comp(q, q.trades[idx*2].kwPerPrice, q.trades[idx*2+1].kwPerPrice))
                cmpIdx = idx*2;
            else 
                cmpIdx = idx*2 +1;
            
            if(comp(q,q.trades[cmpIdx].kwPerPrice, q.trades[idx].kwPerPrice)){
                
                Trade memory tmp = q.trades[idx];
                q.trades[idx] = q.trades[cmpIdx];
                q.trades[cmpIdx] = tmp;
        
                idx = cmpIdx;
            }
            else break;
        }
        return (addr, powerAmount, fee, KwPerPrice);
    }
    
}

contract QueueUserMayBeDeliveryDroneControl is queue {
    Queue requests;
    constructor() public {
        requests.trades.length=200;
        requests.sort = true;
    }
    function setSort(bool sort) public {
        return setSort(requests, sort);
    }
    function addRequest(uint powerAmount, uint d) public {
        push(requests, msg.sender, powerAmount, d);
    }
    function popRequest() public returns (address addr, uint powerAmount, uint fee, uint kwPerPrice) {
        return pop(requests);
    }
    function queueSize() public view returns (uint) {
        return size(requests);
    }
    function queueTop() public view returns (uint){
        return top(requests);
    }
    function getFront() public view returns (uint){
        return getFront(requests);
    }
    function getBack() public view returns (uint){
        return getBack(requests);
    }
    
}
