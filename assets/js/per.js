(function() {
    // Создаём таймер
    setTimeout(function() {
      document.querySelector('body').style.overflow = 'auto';
      var el = document.getElementById('preloader');
      el.remove();

    }, 5500); // 10000 мсек = 10 сек
  })();