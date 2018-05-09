//////////////////////////////////////////////////////////////////////////////////
// Company: Néel institut
// Trainee: Kevin CHIGHINE
//
// Create Date: 22.03.2018
// Design Name:
// Module Name: red_pitaya_haze_block
// Project Name:
// Target Devices:
// Tool Versions:
// Description:
//
// Dependencies:
//
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
//
//////////////////////////////////////////////////////////////////////////////////
/*
###############################################################################
#    pyrpl - DSP servo controller for quantum optics with the RedPitaya
#    Copyright (C) 2014-2016  Leonhard Neuhaus  (neuhaus@spectro.jussieu.fr)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
*/


module red_pitaya_haze_block #(
    //parameters for gain control (binary points and total bitwidth)
   parameter     PSR = 12         ,
   parameter     ISR = 12         ,//official redpitaya: 18

   parameter     GAINBITS = 24    ,
   parameter     FILTERMINBW = 10,

   //enable arbitrary output saturation or not
   parameter     ARBITRARY_SATURATION = 1
)
(
   // data
   input                 clk_i           ,  // clock
   input                 rstn_i          ,  // reset - active low
   input      [ 14-1: 0] dat_i           ,  // input data
   input      [ 14-1: 0] adc_a_i         ,  // ADC data CHA
   input      [ 14-1: 0] adc_b_i         ,  // ADC data CHB
   output     [ 14-1: 0] dat_o           ,  // output data


   // communication with PS
   input      [ 16-1: 0] addr,
   input                 wen,
   input                 ren,
   output reg   		 ack,
   output reg [ 32-1: 0] rdata,
   input      [ 32-1: 0] wdata
);

reg [ GAINBITS-1: 0] set_kp;
reg [ GAINBITS-1: 0] set_kp2;

//  System bus connection
always @(posedge clk_i) begin
   if (rstn_i == 1'b0) begin
      set_kp <= {GAINBITS{1'b0}};
   end
   else begin
      if (wen) begin
         if (addr==16'h108)   set_kp  <= wdata[GAINBITS-1:0];
      end

	  casez (addr)
	     16'h108 : begin ack <= wen|ren; rdata <= {{32-GAINBITS{1'b0}},set_kp}; end
	     16'h200 : begin ack <= wen|ren; rdata <= PSR; end
	     16'h204 : begin ack <= wen|ren; rdata <= ISR; end
	     16'h20C : begin ack <= wen|ren; rdata <= GAINBITS; end
	     16'h228 : begin ack <= wen|ren; rdata <= FILTERMINBW; end

	     default: begin ack <= wen|ren;  rdata <=  32'h0; end
	  endcase
   end
end

reg signed [ 14-1:0] kp_reg        ;
wire  [15+GAINBITS-1: 0] kp_mult1       ;


always @(posedge clk_i) begin
   if (rstn_i == 1'b0) begin
      kp_reg  <= {15+GAINBITS-PSR{1'b0}};
   end
   else begin
      kp_reg <= kp_mult1[15+GAINBITS-1:PSR];
   end
end

assign kp_mult1 = $signed(dat_i) * $signed(set_kp);

assign dat_o = kp_mult1;



endmodule
