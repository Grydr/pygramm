let value = 5 * (3 + 2);
let str = "";

if (value == 25 || value < 30) {
    str = "ok";
} else {
    str = "no";
}

while (value > 0) {
    value -= 1;
}

function compute(a, b) {
    let total = a + b;
    for (let i = 0; i < 3; i += 1) {
        total += i;
    }

    switch (total) {
        case 0:
            total = 100;
            break;
        case 1:
            total = 200;
            break;
        default:
            total = 300;
    }

    return total;
}

let result = compute(2, 3);
let typeName = typeof result;
let dropped = delete result;
let nothing = void result;


return str;
