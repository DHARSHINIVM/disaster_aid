

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title NGO Fund Tracker
/// @notice Enables sponsors to donate to verified NGOs and track how funds are used

contract NGOFundTracker {

    address public owner;

    constructor() {
        owner = msg.sender;
    }

    // Struct to store NGO data
    struct NGO {
        string name;
        bool verified;
        address payable wallet;
    }

    // Mapping: NGO address => NGO details
    mapping(address => NGO) public ngos;

    // Event when NGO is registered
    event NGORegistered(address ngo, string name);

    // Event when donation is made
    event Donation(address sponsor, address ngo, uint amount);

    // Event when usage report is submitted
    event FundUsage(address ngo, string ipfsHash, uint timestamp);

    /// Register NGO (only owner can add)
    function registerNGO(address _wallet, string memory _name) public {
        require(msg.sender == owner, "Only owner can register NGOs");
        require(!ngos[_wallet].verified, "NGO already registered");

        ngos[_wallet] = NGO({
            name: _name,
            verified: true,
            wallet: payable(_wallet)
        });

        emit NGORegistered(_wallet, _name);
    }

    /// Donate to a verified NGO
    function donate(address _ngo) public payable {
        require(ngos[_ngo].verified, "NGO not verified");
        require(msg.value > 0, "Must send ETH");

        ngos[_ngo].wallet.transfer(msg.value);

        emit Donation(msg.sender, _ngo, msg.value);
    }

    /// Submit fund usage log with IPFS hash
    function logUsage(string memory _ipfsHash) public {
        require(ngos[msg.sender].verified, "Not a verified NGO");

        emit FundUsage(msg.sender, _ipfsHash, block.timestamp);
    }

    /// Get NGO details
    function getNGO(address _ngo) public view returns (string memory, bool, address) {
        NGO memory n = ngos[_ngo];
        return (n.name, n.verified, n.wallet);
    }
}
