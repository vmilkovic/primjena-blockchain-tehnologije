pragma solidity ^0.8.0;
// SPDX-License-Identifier: MIT

contract ogranicen_pristup {
    bytes32 pass_hash;
    int stanje;

    constructor(string memory pass){
        pass_hash = sha256(bytes(pass));
        stanje = 500;
    }

    function promijeni_pass(string memory pass, string memory novi_pass) public returns (bool){
        if (pass_hash == sha256(bytes(pass))) {
            pass_hash = sha256(bytes(novi_pass));
            return true;
        } else {
            return false;
        }
    }

    function povecajStanje(string memory pass) public returns (bool){
        if (pass_hash == sha256(bytes(pass))){
            stanje = stanje + 1;
            return true;
        } else {
            return false;
        }
    }

    function smanjiStanje(string memory pass) public returns (bool){
        if (pass_hash == sha256(bytes(pass))){
            stanje = stanje - 1;
            return true;
        } else {
            return false;
        }
    }

    function dohvatiStanje(string memory pass) public view returns (int, bool){
        if (pass_hash == sha256(bytes(pass))){
            return (stanje, true);
        } else {
            return (0, false);
        }
    }
}