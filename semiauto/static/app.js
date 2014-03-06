"use strict";

const SERVER_ADDR = window.location.host;

function $(selector) {
  var els = document.querySelectorAll(String(selector));
  return els.length > 1 ? els : els[0];
};

HTMLElement.prototype.addClass = function(newClass) {
  var oldClasses = this.className;
  this.className = String(this.className + " " + newClass).trim();
};

// Represents tests in a table in the document.
function TestListView(el, tests) {
  this.el = el;
  this.tests = tests;
}

TestListView.prototype = {
  // have a reusable function if we want a 'Re-run tests' option
  resetTable: function() {
    for (var index in this.tests) {
      var test = this.tests[index];
      var rowNode = this.el.insertRow(-1);
      rowNode.id = "test" + test.id;
      var descriptionNode = rowNode.insertCell(0);
      var resultNode = rowNode.insertCell(1);
      descriptionNode.innerHTML = test.description;
      resultNode.addClass("result");
      resultNode.innerHTML = "";
    }
  },

  setTestState: function(testId, outcome, result) {
    var el = $("#test" + testId);
    el.className = outcome;
    if (result) {
      var resultCell = el.getElementsByClassName("result")[0];
      resultCell.innerHTML = result;
    }
  },

  updateTest: function(data) {
    var testData = data.testData;
    switch (testData.event) {
      case "testStart":
        this.setTestState(testData.id, "start");
        break;
      case "success":
        this.setTestState(testData.id, "success", "Pass");
        break;
      case "expectedFailure":
        this.setTestState(testData.id, "success", "Expected failure");
        break;
      case "skip":
        this.setTestState(testData.id, "success", testData.reason);
        break;
      case "error":
        this.setTestState(testData.id, "fail", testData.error);
        break;
      case "failure":
        this.setTestState(testData.id, "fail", testData.error);
        break;
      case "expectedSuccess":
        this.setTestState(testData.id, "fail", "Unexpected success");
        break;
    }
  }
};

function Client(addr) {
  this.addr = addr;
  this.ws, this.testList = null;
}

Client.prototype = {
  sendResponse: function(payload) {
    var respWs = new WebSocket("ws://" + this.addr + "/resp");
    respWs.onopen = function(e) {
      respWs.send(payload);
      console.log("sent: " + payload);
      respWs.close();
      var overlay = $("#overlay");
      overlay.className = "overlay hidden";
    };
  },

  sendUserData: function() { 
    var dialogResponse = $("#dialogResponse");
    var payload = JSON.stringify({"prompt": dialogResponse.value});
    this.sendResponse(payload);
  },

  cancelPrompt: function() { 
    var payload = JSON.stringify({"cancelPrompt": ""});
    this.sendResponse(payload);
  },

  showOverlay: function(text) {
    var dialogText = $("#dialogText");
    var overlay = $("#overlay");
    dialogText.innerHTML = text;
    overlay.className = "overlay"; //remove 'hidden'
  },

  promptUser: function(text) {
    this.showOverlay(text);
    var ok = $("#ok");
    ok.onclick = function() {this.sendUserData()}.bind(this);
  },

  instructUser: function(text) {
    var dialogResponse = $("#dialogResponse");
    dialogResponse.className = "hidden";
    this.showOverlay(text);
    var ok = $("#ok");
    var payload = JSON.stringify({"instructPromptOk": ""});
    ok.onclick = function() {this.sendResponse(payload)}.bind(this);
  },

  connect: function() {
    var cancel = $("#cancel");
    cancel.onclick = function() {this.cancelPrompt()}.bind(this);
    this.ws = new WebSocket("ws://" + this.addr + "/tests");
    this.ws.onopen = function(e) { console.log("opened"); }.bind(this);
    this.ws.onclose = function(e) { console.log("closed"); }.bind(this);
    this.ws.onmessage = function(e) {
      var data = JSON.parse(e.data);
      if (data.testList) {
        // set up the test_list table
        this.testList = new TestListView($("#test_list"), data.testList);
        this.testList.resetTable();
      }
      else if (data.testRunStart) {
        // TODO: I don't receive this message for some reason
        document.getElementById("notification").innerHTML = "Running tests";
      }
      else if (data.testRunStop) {
        // TODO: I don't receive this message for some reason
        document.getElementById("notification").innerHTML = "Done";
      }
      else if (data.prompt) {
        // handle request for user data
        this.promptUser(data.prompt);
      }
      else if (data.instructPrompt) {
        this.instructUser(data.instructPrompt);
      }
      else if (data.updateTest){
        // TODO: this assumes any other request will be to update the table
        this.testList.updateTest(data.updateTest);
      }
    }.bind(this);
  },

  emit: function(event, data) {
    var payload = JSON.stringify({event: data});
    console.log("Sending " + payload);
    this.ws.send(payload);
  }
};

function App(server) {
  this.addr = server;
  this.client = new Client(this.addr);
}

App.prototype = {
  start: function() {
    this.client.connect();
  }
};

function init() {
  var app = new App(SERVER_ADDR);
  app.start();
}

document.addEventListener("DOMContentLoaded", init, false);
