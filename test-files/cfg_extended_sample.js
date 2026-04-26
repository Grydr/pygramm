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
