////////////////////////////////////////////////////////////
// This is an example contract hacked together at a meetup.
// It is by far not complete and only used to show some
// features of Solidity.
////////////////////////////////////////////////////////////
pragma solidity ^0.4.24;

contract PriorityQueue
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
    
    function size(Queue storage q) constant internal returns (uint) {
        if(q.back < q.front)
            return capacity(q) - q.front + q.back;
        else 
            return q.back - q.front;
    }
    
    function push(Queue storage q, address addr, uint powerAmount, uint data) internal
    {
        if ((q.back + 1) % q.trades.length == q.front)
            return; // throw;
        
        uint idx = q.back;
        
        q.trades[idx].addr = addr;
        q.trades[idx].powerAmount = powerAmount;
        q.trades[idx].fee = data;
        q.trades[idx].kwPerPrice = data * 8192 / powerAmount;
        
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
