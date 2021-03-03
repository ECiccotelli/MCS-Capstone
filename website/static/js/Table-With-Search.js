//Table with search
$(document).ready(function() {
  $(".search").keyup(function () {
    var searchTerm = $(".search").val();
    var listItem = $('.results tbody').children('tr');
    var searchSplit = searchTerm.replace(/ /g, "'):containsi('")
    
  $.extend($.expr[':'], {'containsi': function(elem, i, match, array){
        return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
    }
  });
    
  $(".results tbody tr").not(":containsi('" + searchSplit + "')").each(function(e){
    $(this).attr('style','display:none');
  });

  $(".results tbody tr:containsi('" + searchSplit + "')").each(function(e){
    $(this).attr('style','display:true');
  });

  var jobCount = $('.results tbody tr[visible="true"]').length;
    $('.counter').text(jobCount + ' item');
  if(jobCount == '0') {$('.no-result').show();}
    else {$('.no-result').hide();}
		  });
});


$('input[name="checkbox"]:checkbox').on('change', function() {
    if (this.checked){
        $(this).closest('tr').each(function() {
            var cells = $('td', this);
            $('#dataTable1').append('<tr><td>' + cells.eq(1).text() + '</td></tr>');
        });
    } else {
        $(this).closest('tr').each(function() {
            var cells = $('td', this);
            var id = cells.eq(0).text();
            $('#' + id).closest('tr').remove();
        });
    };
});

$('input[name="checkbox_mylist"]:checkbox').on('change', function() {
    console.log('change')
    if (!(this.checked)){
        console.log('unchecked')
         $('input[name="checkbox"]:checkbox').closest('tr').each(function() {
            var cells = $('td', this);
            var id = cells.eq(0).text()
            console.log(id)
            $('#' + id, this).prop("checked", false);
         });
    }
});

/*$('input[name="checkbox"]:checked').closest('tr').each(function() {
    var cells = $('td', this);
    console.log(cells)
    $('#dataTable1').append('<tr><td>' + cells.eq(0).text() +
        '</td><td>' + cells.eq(1).text() + '</td></tr>');
});*/