$(function () {

  /* Functions */

  function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
  }

  function setCookie(name, value, options = {}) {

    options = {
      path: '/',
      secure: true,
      'max-age': 3600
    };

    if (options.expires instanceof Date) {
      options.expires = options.expires.toUTCString();
    }

    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);

    for (let optionKey in options) {
      updatedCookie += "; " + optionKey;
      let optionValue = options[optionKey];
      if (optionValue !== true) {
        updatedCookie += "=" + optionValue;
      }
    }

    document.cookie = updatedCookie;
  }

  function deleteCookie(name) {
    setCookie(name, "", {
      'max-age': -1
    })
  }


  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal .modal-content").html("");
        $("#modal").modal("show");
      },
      success: function (data) {
        $("#modal .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          if (data.html_form){
            $("#modal .modal-content").html(data.html_form);
          }else{
              $(".messages-block").html(data.html_messages_block)
              $("#modal").modal("hide");
              if (data.html_header){
                  $('#header').html(data.html_header)
              }
              if (data.html_profile_block){
                  $('.profile-data-block').html(data.html_profile_block)
              }
          }
        }
        else {
          $(".messages-block").html(data.html_messages_block)
          $("#modal .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

  var loadBasketForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $(".shopping-cart-button").removeClass('show').addClass('fade')
        $(".basket-active").removeClass('fade').addClass('show')
      },
      success: function (data) {
        $(".basket-active").html(data.html_form);

      }
    });
  };

  var closeBasketForm = function () {
    $(".basket-active").html('');
    $(".shopping-cart-button").removeClass('fade').addClass('show')
    $(".basket-active").removeClass('show').addClass('fade')
  };

  var closeBasketFormIfOpened = function () {
    if ($('.basket-active').hasClass('show')) {
        closeBasketForm()
    }else {
      closeBasketForm()
    }
  }

  var priceUpdate = function () {
    let el = $(this);
    let price = el.siblings()[3]
    let summ = 0
    price.textContent = Number((el[0].value * el.siblings()[1].textContent).toFixed(2));
    let summ_arr = document.getElementsByClassName('one-book-summ')
    for (let i = 0; i < summ_arr.length; i++) {
      summ += parseFloat(summ_arr[i].textContent)
    }
    if (el[0].value == el[0].max || el[0].value == 0){
      el.addClass('max-count')
    }else{
      el.removeClass('max-count')
    }
    $('.calculated-price')[0].textContent = Number((summ).toFixed(2));
    $('#price')[0].textContent = Number((summ).toFixed(2));
  };

  function clearOrderList(){
    $(".basket-active").html('');
  }


  var addToBasket = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.updated_basket){
          document.cookie = `basket=${data.updated_basket}`
        }
        if ($(".basket-active").hasClass('show')){
          $(".basket-active").html(data.html_basket_form)
          $(".basket-active").addClass('show')
        }else {
          $(".basket").html(data.html_basket_button)
          $(".basket-active").html('')
        }



      }
    });
    return false;
  };

  var orderDetail = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal .modal-content").html("");
        $("#modal").modal("show");
      },
      success: function (data) {
        $("#modal .modal-content").html(data.hrml_order);
      }
    });
  };

  var filterBooks = function () {
    let form = $(this).parent()
    let action = form.attr("action")
    if (action.indexOf('?')){
      action = action.split('?')[0]
    }
    if ($(this)[0].value){
      form[0].action = `${form.attr("action")}?sub_string=${$(this)[0].value}`
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        $('.filtered-books').html(data.html_filtered_books)
        form[0].action = action
      }
    });
    return false;
  }else {
      $('.filtered-books').html('')
    }
  }

  var clearBasket = function () {
    document.cookie = 'basket' + '=; Max-Age=0'
    $(".basket-active").html('').addClass('fade').removeClass('show')
    $(".shopping-cart-button").addClass('fade')
  };


  var removeFromBasket = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        console.log('UpD DEELETE')
        if (data.updated_basket) {
          document.cookie = `basket=${data.updated_basket}`
          if ($(".basket-active").hasClass('show')) {
            $(".basket-active").html(data.html_basket_form)
            $(".basket-active").addClass('show')
          } else {
            $(".basket").html(data.html_basket_button)
            $(".basket-active").html('')
          }


        }else {
          $(".basket").html(data.html_basket_button)
          $(".basket-active").html('')
        }
      }
    });
    return false;
  };




  /* Binding */

  $(window).on('load', clearOrderList)
  $(window).on('load', closeBasketForm)

  // auth
  // Sign Up Modal Form Handler
  $("body").on("click", "#sign-up-button", loadForm);
  $("#modal").on("submit", ".sign-up-form", saveForm);

  // Log In Modal Form Handler
  $("body").on("click", "#log-in-button", loadForm);
  $("#modal").on("submit", ".log-in-form", saveForm);

  // Change Password Modal Form Handler
  $("body").on("click", "#change-password-button", loadForm);
  $("body").on("submit", ".check-password-form", saveForm)
  $("body").on("submit", ".change-password-form", saveForm)

  // Change Email Modal Form Handler
  $("body").on("click", "#change-email-button", loadForm);
  $("body").on("submit", ".change-email-form", saveForm)


  // main
  // Add Book to the basket
  // $("body").on("click", ".add-to-basket", addCookie)
  // $("body").on("click", ".add-to-basket", test)

  $("body").on("click", '.main-container', closeBasketFormIfOpened);
  $("body").on("click", ".shopping-cart-button", loadBasketForm);
  $("body").on("click", ".exit-button", closeBasketForm);
  $("body").on("click", "#offer-button", closeBasketForm);


  $("body").on("change", ".books-count", priceUpdate);

  $("body").on("click", ".order-detail-button", orderDetail);

  $("body").on("click", ".add-to-basket", addToBasket);

  $("body").on("click", ".remove-from-basket", removeFromBasket);

  $("body").on("click", ".clear-basket", clearBasket);

  $("body").on("input", ".search-book", filterBooks);

  // $(".add-to-basket").click(addToBasket)

});