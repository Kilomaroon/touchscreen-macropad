module frontBezel() {
    translate([3,3,3.8])
        import("adafruit-2354-7in-tft-touchscreen-front-bezel.stl");
}

module arduino() {
    import("Arduino_Bumper_0005.stl");
}

difference() {
union() {
    translate([0.385,0,0])
    union(){
        translate([-5,0,15])
        rotate([0,-120,0])
            frontBezel();

        translate([-5,0,7])
        rotate([0,-120,0])
        translate([-2.5,0,-4])
            cube([10,171,12.8]);
    }
    translate([-122.6,0,0])
        cube([122.6,171,7]);
    
    translate([-64.37,0,97.9])
    rotate([0,-150,0])
        cube([5,1.5,110]);
    
    translate([-64.37,169.5,97.9])
    rotate([0,-150,0])
        cube([5,1.5,110]);
    
    translate([-80,45,6])
    rotate([0,0,90])
        arduino();
}

translate([0,-5,0])
    cube([10,200,10]);

translate([-132.6,-5,0])
    cube([10,200,20]);
}