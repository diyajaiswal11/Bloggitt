function toggle() {
    let bts = document.getElementsByClassName('btn')
    for (let btn of bts) {
      if (btn.classList.contains('btn-success')) {
        btn.classList.remove('btn-success')
        btn.classList.add('btn-danger')
        btn.innerHTML = 'Delete from Favourites'
      }
      else {
        btn.classList.remove('btn-danger')
        btn.classList.add('btn-success')
        btn.innerHTML = 'Add To Favourites'
      }
    }
  }

  $('.btn').click(function () {
    var slug;
    slug = $(this).attr("data-slug");
    $.ajax(
      {
        type: "GET",
        url: `/detail/${slug}/Favourites`,
        success: function (data) {
          console.log("Success")
        }
      })
  });