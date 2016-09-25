"use strict";

var IO_ARRAY = $("#io_array");
var IO_PERMUTATIONS = $("#io_permutations");
var BTN_STOP_GENERATOR = $("#btn_stop_gnerator");
var MESSAGE_ELEMENT = $("#message");

var STATUS_WAIT_FOR_POST_ARRAY = 1;
var STATUS_READY_FOR_RECEIVING_NEXT_PERMUTATION = 2;

var status = STATUS_WAIT_FOR_POST_ARRAY;


$(function() {
    $('#next_permutation').bind('click', nextPermutation);
});


function nextPermutation() {
    //console.log(status);
    try {
        if (status == STATUS_WAIT_FOR_POST_ARRAY) {
            var data;
            try {
                data = readArrayFromTextArea();
            } catch(e) {
                alert('Ошибка ' + e.name + ":" + e.message + "\n" + e.stack);
                data = null;
            }
            if (data === null) {
                displayMessage("Ошибка в ведённых данных!");
            } else {
                postArray(data);
            }
        }
        else {
            getNextPermutation();
        }
    } catch(e) {
        alert('Ошибка ' + e.name + ":" + e.message + "\n" + e.stack);
    }
    return false;
};

function readArrayFromTextArea(){
    var data = IO_ARRAY.val().trim();

    if (data.length == 0) {
        data = [];
    } else {
        data = data.split(' ');

        for (var i = 0; i < data.length; i++) {
            data[i] = parseInt(data[i]);
            if (!(data[i] > 0)) {
                return null;
            }
        }
    }
    return JSON.stringify(data, null);
}

function postArray(data){
     $.ajax({
        type : "POST",
        url : POST_ARRAY_URL,
        data: data,
        contentType: 'application/json; charset=UTF-8',
        success: onPostArrayAjaxSuccess
    });
}

function onPostArrayAjaxSuccess(data, status) {
    if (data.length > 0 && data[0] == "[" ) {
        BTN_STOP_GENERATOR.removeAttr("hidden");
        window.status = STATUS_READY_FOR_RECEIVING_NEXT_PERMUTATION;
    }
    showNextPermutation(data);
}

function showNextPermutation(next_permutation) {
    IO_PERMUTATIONS.append(
        '<li class="permutation">' + next_permutation + '</li>'
    );
}

function getNextPermutation(){
     $.ajax({
        type : "GET",
        url : NEXT_PERMUTATION_URL,
        contentType: 'application/json; charset=UTF-8',
        success: onGetNewPermutationAjaxSuccess
    });
}

function onGetNewPermutationAjaxSuccess(data, status) {
    showNextPermutation(data);
}


function displayMessage(message) {
    MESSAGE_ELEMENT.append("<br>" + message);
}