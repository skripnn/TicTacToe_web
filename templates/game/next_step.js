setTimeout(function(){
  const xhr = new XMLHttpRequest();

  xhr.open('POST', '', true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');

  xhr.send();
  xhr.onload = () => location.reload();

  }, 100);
