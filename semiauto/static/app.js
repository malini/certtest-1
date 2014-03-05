"use strict";

const SERVER_ADDR = window.location.host;

// TODO: This didn't succeed at retrieving elements, like $("test_list")
function $(selector) {
  var els = document.querySelectorAll(selector);
  return els.length > 1 ? els : els[0];
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
      rowNode.id = test.id;
      var descriptionNode = rowNode.insertCell(0);
      var resultNode = rowNode.insertCell(1);
      descriptionNode.innerHTML = test.description;
      resultNode.id = test.id + "result";
      resultNode.innerHTML = "";
    }
  },

  setTestState: function(test_id, color) {
    document.getElementById(test_id).style.background = color;
  },

  updateTest: function(data) {
    //TODO: I propose we use {"updateResult" {"type": "success", id:"id", ...}}
    // so I can use a nice switch case here instead of all these ifs!
    if (data.testStart) {
      this.setTestState(data.testStart.id, "yellow");
    }
    else if (data.success) {
      this.setTestState(data.success.id, "green");
    }
    else if (data.expectedFailure) {
      this.setTestState(data.expectedFailure.id, "green");
    }
    else if (data.skip) {
      this.setTestState(data.skip.id, "grey");
      document.getElementById(data.skip.id + "result").innerHTML = data.skip.reason;
    }
    else if (data.error) {
      this.setTestState(data.error.id, "red");
      document.getElementById(data.error.id + "result").innerHTML = data.error.error;
    }
    else if (data.failure) {
      this.setTestState(data.failure.id, "red");
      document.getElementById(data.failure.id + "result").innerHTML = data.failure.error;
    }
    else if (data.unexpectedSuccess) {
      this.setTestState(data.unexpectedSuccess.id, "red");
    }
    else {
      console.log("got: " + data);
    }
  },
};

function Client(addr) {
  this.ws;
  this.testList;
  this.addr = addr;
}

Client.prototype = {
  connect: function() {
    this.ws = new WebSocket("ws://" + this.addr + "/tests");
    this.ws.onopen = function(e) { console.log("opened"); }.bind(this);
    this.ws.onclose = function(e) { console.log("closed"); }.bind(this);
    this.ws.onmessage = function(e) {
      var data = JSON.parse(e.data);
      for (var i in data) {
        console.log(data[i]);
      }
      if (data.testList) {
        // set up the test_list table
        this.testList = new TestListView(document.getElementById("test_list"), data.testList);
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
        var response = window.prompt(data.prompt);
        var payload = JSON.stringify({"prompt": response});
        var respWs = new WebSocket("ws://" + this.addr + "/resp");
        respWs.onopen = function(e) {
          respWs.send(payload);
          console.log("sent: " + payload);
          respWs.close();
        };
      }
      else {
        // TODO: this assumes any other request will be to update the table
        this.testList.updateTest(data);
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
