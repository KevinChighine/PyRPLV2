# PyRPLV2
Python Red Pitaya Lockbox program modified with 2 IQ modules and 4 proportional modules
 *
 *
 *        /---\            /---\      /---\
 *   IN1--|IQ1|-------+--> |P1 | ---> | + | ---> OUT1
 *        \---/       |    \---/      \---/
 *                    |                 ^  
 *                    |    /---\        |  
 *                +---|--> |P1'| ------- 
 *                |   |    \---/            
 *                |   |                    
 *        /---\   |   |    /---\      /---\
 *   IN2--|IQ2|---+   +--> |P2 | ---> | + | ---> OUT2
 *        \---/   |        \---/      \---/
 *                |                     ^  
 *                |        /---\        |  
 *                +----->  |P2'| -------- 
 *                         \---/            