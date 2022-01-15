pragma solidity ^0.7.0;

// SPDX-License-Identifier: MIT

contract BrojacStanja {
    int256 public stanje;

    constructor() {
        stanje = 500;
    }

    function povecajStanje() public {
        stanje = stanje + 1;
    }

    function smanjiStanje() public {
        stanje = stanje - 1;
    }
}
