/*
"use strict";

const SERVER_ADDR = window.location.host;

function $(selector) {
  var els = document.querySelectorAll(selector);
  return els.length > 1 ? els : els[0];
};

// TODO(ato): Simplify to a dict
var Test = function(t) {
  var self = {
    description: t.description,
    outcome: "unknown"
  };

  self.init();
  return self;
};

// Tests is a model that contains individual Tests.  It allows tests
// to be added and for callbacks to be defined for when they are.
var Tests = function() {
  var tests = [];
  var onNewTest;

  var self = {
    init: function() {},

    add: function(test, cb) {
      tests.push(test);
      if (cb && typeof(cb) === "function")
        cb(test);
    }
  };

  self.init();
  return self;
};

// Represents a single test row in the TestListView table.
var TestView = function(el) {
  var $el = el;

  var self = {
    init: function() {}
  };

  self.init();
  return self;
};

// Represents tests in a table in the document.  It registers
// callbacks on the model, and updates the test list appropriately
// when a test is added or a test's state changes.
var TestListView = function(el, model) {
  var $el = el;
  var tests = model;

  var self = {
    init: function() {
      tests.onTestRunStart = self.newTestRun;
      tests.onNewTest = self.insertTest;
      tests.onTestRunStop = self.insertSummary;
    },

    newTable: function() {
      alert("creating new table!");
    },

    insertTest: function(test) {
      alert("inserting new test row");
    },

    insertSummary: function() {
      alert("inserting summary");
    }
  };

  self.init();
  return self;
};

var Client = function(addr) {
  var ws;

  var self = {
    init: function() {},

    connect: function() {
      ws = new WebSocket("ws://" + addr + "/tests");
      ws.onopen = function(e) { console.log("opened"); };
      ws.onclose = function(e) { console.log("closed"); };
      ws.onmessage = function(e) {
        if (e.data == "prompt") {
          self.emit("prompt", "Hi, I'm user data");
        }
      };
    },

    emit: function(event, data) {
      var payload = JSON.stringify({event: data});
      console.log("Sending " + payload);
      ws.send(payload);
    }
  };

  self.init();
  return self;
};

var App = function(root, server) {
  var $el = root;
  var addr = server;
  var tests, testList, client;

  var self = {
    init: function() {
      tests = Tests();
      testList = TestListView($("test_list"), tests);
      client = Client(addr);
    },

    start: function() {
      client.connect();
    }
  };

  self.init();
  return self;
};

function init() {
  var app = App($("body"), SERVER_ADDR);
  app.start();
}

document.addEventListener("DOMContentLoaded", init, false);
*/

var ws;

window.onload = function() {
  ws = new WebSocket("ws://localhost:6666/tests");
  ws.onopen = function(e) { console.log("opened"); };
  ws.onclose = function(e) { console.log("closed"); };
  ws.onmessage = function(e) {
    console.log("received: " + e.data);
    var data = JSON.parse(e.data);
    if (data.prompt) {
      var response = window.prompt(data.prompt);
      var payload = JSON.stringify({"prompt": response});
      ws_resp = new WebSocket("ws://localhost:6666/resp");
      ws_resp.onopen = function(e) { console.log("opened resp"); ws_resp.send(payload);console.log("sent: " + payload);};
    }
  };
};
