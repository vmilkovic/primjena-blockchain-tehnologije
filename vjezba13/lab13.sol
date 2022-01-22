pragma solidity ^0.4.21;

// SPDX-License-Identifier: MIT

contract Hello {
    string public message;
    string public message2;

    constructor() public {
        message = "vanilija";
        message2 = "cokolada";
    }

    function setMessage(string newMessage) public {
        message = newMessage;
    }

    function setMessage2(string newMessage) public {
        message2 = newMessage;
    }

    function vrati() public view returns (string) {
        return message2;
    }
}
