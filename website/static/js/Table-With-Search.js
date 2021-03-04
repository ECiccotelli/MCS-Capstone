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
    var $this = $(this);
    var row = $this.closest('tr');

    if (this.checked){
        $(this).closest('tr').each(function() {
            var cells = $('td', this);
            $('#dataTable1').append('<tr><td>' + cells.eq(1).text() + '</td><td style="text-align: right;" class="custom-control custom-checkbox"><input class="custom-control-input" name="checkbox_mylist" type="checkbox" id="' + cells.eq(0).text() + '" checked><label class="custom-control-label" for="' + cells.eq(0).text() + '"></label></td></tr>');
            row.insertBefore( row.parent().find('tr:first-child') );
        });
    } else {
        $(this).closest('tr').each(function() {
            var cells = $('td', this);
            var id = cells.eq(0).text();
            $('#' + id).closest('tr').remove();
            row.insertAfter( row.parent().find('tr:last-child') );
        });
    };
});

$("#btnSave2").click(function() {
        html2canvas($("#schedule_main"), {
          onrendered: function(canvas) {
            document.body.appendChild(canvas);

                // Convert and download as image
                Canvas2Image.saveAsPNG(canvas);
          }
        });
      });

      function saveAs(uri, filename) {
        var link = document.createElement('a');
        if (typeof link.download === 'string') {
          link.href = uri;
          link.download = filename;

          //Firefox requires the link to be in the body
          document.body.appendChild(link);

          //simulate click
          link.click();

          //remove the link when done
          document.body.removeChild(link);
        } else {
          window.open(uri);
        }
      }

/*$('input[name="checkbox"]:checked').closest('tr').each(function() {
    var cells = $('td', this);
    console.log(cells)
    $('#dataTable1').append('<tr><td>' + cells.eq(0).text() +
        '</td><td>' + cells.eq(1).text() + '</td></tr>');
});*/