var message = document.currentScript.getAttribute('message');
var category = document.currentScript.getAttribute('category');

document.addEventListener("DOMContentLoaded", function(){
  const notyf = new Notyf({
      position: {
          x: 'right',
          y: 'bottom',
      },
      types: [
          {
              type: 'info',
              background: 'blue',
              icon: {
                  className: 'fas fa-info-circle',
                  tagName: 'span',
                  color: '#fff'
              },
              dismissible: true,
              duration: 5000
          },
          {
              type: 'error',
              background: 'red',
              icon: {
                  className: 'fas fa-times',
                  tagName: 'span',
                  color: '#fff'
              },
              dismissible: true,
              duration: 5000
          },
          {
              type: 'warning',
              background: 'orange',
              icon: {
                  className: 'fas fa-exclamation-triangle',
                  tagName: 'span',
                  color: '#fff'
              },
              dismissible: true,
              duration: 5000
          },
          {
              type: 'success',
              background: 'green',
              icon: {
                  className: 'fas fa-check',
                  tagName: 'span',
                  color: '#fff'
              },
              dismissible: true,
              duration: 5000
          }
      ]
  });

  if (category == "error"){
    notyf.open({
      type: 'error',
      message: message,
    });
  }
  else if (category == "info"){
    notyf.open({
      type: 'info',
      message: message,
    });
  }
  else if (category == "warning"){
    notyf.open({
      type: 'warning',
      message: message,
    });
  }
  else if (category == "success"){
    notyf.open({
      type: 'success',
      message: message,
    });
  }
});
