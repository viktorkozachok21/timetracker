//hamburger button animation in menu
$(document).on("click", ".first-button", function() {
  $('.animated-icon1').toggleClass('open');
});

//get_message for worker
$(document).on("click", "#account", function() {
  $.ajax({
      type: 'GET',
      url: '{% url "get_messages" %}',
      data: {
        'worker': $('#user_name').attr("alt"),
      },
      success: function(response) {
        $("#messages-box").html(response.messages_html);
    }
  });
});

//mesage to_trash
$(document).on("click", ".fa-trash-alt", function() {
      $.ajax({
        type: 'POST',
        url: "{% url 'to_trash' %}",
        data: {
          'worker': $('#user_name').attr("alt"),
          'message': $(this).attr("alt"),
          'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(response) {
          $("#messages-box").html(response.messages_html);
      }
    });
  return false;
});

//show new commwnt form
$(document).ready(function(){
    $(".fa-plus-square").click(function(){
      $('#modalCommentForm').modal('show');
      $('#hide').attr("title", this.id);
    });
});

//add new comment
$(document).ready(function() {
  $('#comment-form').submit(function(event) {
    event.preventDefault();
      $.ajax({
        type: 'POST',
        url: "{% url 'add_comment' project.id %}",
        data: {
          'comment': $('#comments').val(),
          'author': $('#user_name').html(),
          'task': $('#hide').attr("title"),
          'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(response) {
          var id = "#more" + $('#hide').attr("title");
          $(id).html(response.comments_html);
      }
    });
  resetForm();
  return false;
});
);

//reset comment form
function resetForm() {
  $('#comments').val('');
  $('#modalCommentForm').modal('hide');
};

//show all comments for task
$(document).on("click", ".more", function() {
      var self = $(this);
      $.ajax({
          type: 'GET',
          url: '{% url "show_comments" project.id %}',
          data: {
            'task': self.attr("alt")
          },
          success: function(response) {
            var id = "#more" + self.attr("alt");
            $(id).html(response.comments_html);
        }
      });
  });

//save changes of task summary
$(document).on("click", ".fa-save", function() {
    var id = "#content" + $(this).attr("alt");
      $.ajax({
        type: 'POST',
        url: "{% url 'save_task' project.id %}",
        data: {
          'summary': $(id).html(),
          'worker': $('#user_name').attr("alt"),
          'task': $(this).attr("alt"),
          'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(response) {
          $(id).html(`${response.task.summary}`);
          $("#messages-box").html(response.task.messages_html);
      }
    });
  return false;
});

//end working on task
$(document).on("click", ".fa-pause-circle", function() {
    var end = $(this);
      $.ajax({
        type: 'POST',
        url: "{% url 'end_task' project.id %}",
        data: {
          'worker': $('#user_name').attr("alt"),
          'task': end.attr("alt"),
          'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(response) {
          var status = "#task_status" + end.attr("alt");
          var worker = "#task_worker" + end.attr("alt");
          $(status).html(`<i class="far fa-check-square" title="start" alt="${response.task.task}"></i>`).fadeIn(500);
          $(worker).html('Worker: the task is free');
      }
    });
  return false;
});

//start working on task
$(document).on("click", ".fa-check-square", function() {
    var start = $(this);
      $.ajax({
        type: 'POST',
        url: "{% url 'start_task' project.id %}",
        data: {
          'worker': $('#user_name').attr("alt"),
          'task': start.attr("alt"),
          'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(response) {
          var status = "#task_status" + start.attr("alt");
          var worker = "#task_worker" + start.attr("alt");
          $(status).html(`<i class="far fa-pause-circle" title="end" alt="${response.task.task}"></i>`).fadeIn(500);
          $(worker).html(`Worker: ${response.task.worker}`);
      }
    });
  return false;
});

//close task
$(document).on("click", ".fa-window-close", function() {
  var start = $(this);
    $.ajax({
      type: 'POST',
      url: "{% url 'completed_task' project.id %}",
      data: {
        'task': start.attr("alt"),
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
      },
      success: function(response) {
        window.location.href = response.url;
    }
  });
});

//open closed task
$(document).on("click", ".fa-calendar-plus", function() {
  var start = $(this);
    $.ajax({
      type: 'POST',
      url: "{% url 'open_task' project.id %}",
      data: {
        'task': start.attr("alt"),
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
      },
      success: function(response) {
        window.location.href = response.url;
    }
  });
});

//get timelogs for task
$(document).on("click", ".fa-clock", function() {
    var self = $(this);
    $.ajax({
        type: 'GET',
        url: '{% url "get_time_logs" project.id %}',
        data: {
          'task': self.attr("alt")
        },
        success: function(response) {
          $("#time-logs").html(response.timelogs_html);
          $('#timeLogForm').modal('show');
      }
    });
});
