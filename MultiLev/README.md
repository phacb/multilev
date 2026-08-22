An annotated image of a fully built MultiLev device can be found in MultiLev.pdf. 

MultiLev is based on the original tinylev (https://www.instructables.com/Acoustic-Levitator/) with individually addressed transducers as in Ultraino (https://www.instructables.com/Ultrasonic-Array/). 

The phases are controlled using 9 x pi-picos and driver board (design included in this repository) to control the phases of each transducer individually.

The stl files needed for MultiLev are included in the stl directory.

- top-array.stl --> the top array (prints best with the solid long edge as the base)
- bottom-array.stl --> the lower array (prints best with the solid long edge as the base)
- gantry base --> the gantry's holding the stepper motors and the GBRL controller are fixed to this
- gantry.stl --> x2 needed - the gantry that the stepper motors are attached to (prints best with the flat edges of the legs as the base)
- flange.stl --> x2 needed - the flange to hold the rotational bearings in place (prints best on its long thin edge as the base)
- base.stl --> the base which the assembled levitator slots into
- mosfet-plate.stl --> the plate that goes onto the base for the mosfet connectors
- mosfet-plate-bottom.slt --> for holding the soldered mosfet header board in place

MultiLev is designed for 10 mm 40 kHz transducers, e.g., https://manorshi.en.alibaba.com/product/60248714908-801018150/10mm_40khz_piezo_ultrasonic_Transmitter_Receiver_sensor.html?spm=a2700.8304367.rect38f22d.1.2a14fee7WhfcRq (choose the 40khz T option). Check the polarity as in the tinylev instructables!

The separation of the arrays are approximately 11.5 cm. The stepper motors, controlled using the GRBL controller, are used to adjust the height, which is optimised when the current is maximised.

Additional components required for constructing the levitator are:

- 6 mm steel rod

- Flange coupling connectors: https://www.amazon.co.uk/Coupling-Connector-Coupler-Accessory-Fittings/dp/B0833NTD9M?th=1

- T8 lead screw (1mm) https://www.amazon.co.uk/Tenlacum-Printer-Thread-Copper-Stepper/dp/B07TKGMZN9?th=1

- T8 lead screw nut (1mm) https://www.amazon.co.uk/Lt-lead-screw-Trapezoidal-Screw-Copper/dp/B08DXZ1792?th=1

- 8 mm to 6 mm couplers (for the lead screw to the 6 mm rod): https://www.amazon.co.uk/sourcing-map-Coupling-L25xD14-Connector/dp/B07P82CG1Q?th=1

- linear bearings: https://www.amazon.co.uk/sourcing-map-Flange-Linear-Bearings/dp/B07H952BCY?th=1

- rotational bearings: https://www.amazon.co.uk/dp/B0CGDT88MD?th=1

- 6mm to 5 mm rotatable coupler (for the stepper motor) https://www.amazon.co.uk/gp/product/B09KNBXZD8?th=1

- GRBL controller: https://www.amazon.co.uk/RATTMMOTOR-Connection-Controller-Engraving-Maschine/dp/B08MTRVKZZ/

- Stepper motors: https://www.amazon.co.uk/gp/product/B0814T3L6J/ref=ppx_yo_dt_b_asin_title_o06_s00?ie=UTF8&th=1
