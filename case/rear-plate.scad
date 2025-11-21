module original() {
    translate([1.5,1.5,-5.5])
    import("adafruit-2354-7in-tft-touchscreen-rear-bezel.stl");
}
difference() {
    original();
    translate([1.3,1.3,1])
        cube([100.4,165.4,5]);
    
    translate([0,-0.1,0])
        cube([120,0.4,5]);
    translate([-0.1,0,0])
        cube([0.4,200,5]);
    translate([102.7,0,0])
        cube([0.4,200,5]);
    translate([167.8,0,0])
        cube([120,0.4,5]);
}
