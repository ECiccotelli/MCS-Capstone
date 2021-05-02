var mainRun = function (reload) {
	function ScheduleTemplate( element ) {
		this.element = element;
		this.timelineItems = this.element.getElementsByClassName('cd-schedule__timeline')[0].getElementsByTagName('li');
		this.timelineStart = getScheduleTimestamp(this.timelineItems[0].textContent);
		this.timelineUnitDuration = getScheduleTimestamp(this.timelineItems[1].textContent) - getScheduleTimestamp(this.timelineItems[0].textContent);
		this.topInfoElement = this.element.getElementsByClassName('cd-schedule__top-info')[0];
		this.singleEvents = this.element.getElementsByClassName('cd-schedule__event');
		this.modal = this.element.getElementsByClassName('cd-schedule-modal')[0];
		this.modalHeader = this.element.getElementsByClassName('cd-schedule-modal__header')[0];
		this.modalHeaderBg = this.element.getElementsByClassName('cd-schedule-modal__header-bg')[0];
		this.modalBody = this.element.getElementsByClassName('cd-schedule-modal__body')[0];
		this.modalBodyBg = this.element.getElementsByClassName('cd-schedule-modal__body-bg')[0];
		this.modalClose = this.modal.getElementsByClassName('cd-schedule-modal__close')[0];
		this.modalDate = this.modal.getElementsByClassName('cd-schedule-modal__date')[0];
		this.modalEventName = this.modal.getElementsByClassName('cd-schedule-modal__name')[0];
		this.coverLayer = this.element.getElementsByClassName('cd-schedule__cover-layer')[0];

		this.modalMaxWidth = 800;
		this.modalMaxHeight = 480;

		this.animating = false;
		this.supportAnimation = Util.cssSupports('transition');

		this.initSchedule();
	};

	ScheduleTemplate.prototype.initSchedule = function() {
		this.scheduleReset();
		this.initEvents();
	};

	ScheduleTemplate.prototype.scheduleReset = function() {
		// according to the mq value, init the style of the template
		var mq = this.mq(),
			loaded = Util.hasClass(this.element, 'js-schedule-loaded'),
			modalOpen = Util.hasClass(this.modal, 'cd-schedule-modal--open');
		if( mq == 'desktop' && !loaded ) {
			Util.addClass(this.element, 'js-schedule-loaded');
			this.placeEvents();
			modalOpen && this.checkEventModal(modalOpen);
		} else if( mq == 'desktop' && reload) {
			reload = false;
			Util.addClass(this.element, 'js-schedule-loaded');
			this.placeEvents();
			modalOpen && this.checkEventModal(modalOpen);
		} else if( mq == 'mobile' && loaded) {
			//in this case you are on a mobile version (first load or resize from desktop)
			Util.removeClass(this.element, 'cd-schedule--loading js-schedule-loaded');
			this.resetEventsStyle();
			modalOpen && this.checkEventModal();
		} else if( mq == 'desktop' && modalOpen ) {
			//on a mobile version with modal open - need to resize/move modal window
			this.checkEventModal(modalOpen);
			Util.removeClass(this.element, 'cd-schedule--loading');
		} else {
			Util.removeClass(this.element, 'cd-schedule--loading');
		}
	};

	ScheduleTemplate.prototype.resetEventsStyle = function() {
		// remove js style applied to the single events
		for(var i = 0; i < this.singleEvents.length; i++) {
			if (this.singleEvents[i].style.display == 'none'){
				this.singleEvents[i].removeAttribute('style');
				this.singleEvents[i].style.display = 'none'

			} else {
				this.singleEvents[i].removeAttribute('style');
			}


		}
	};

	ScheduleTemplate.prototype.placeEvents = function() {
		// on big devices - place events in the template according to their time/day
		var self = this,
			slotHeight = this.topInfoElement.offsetHeight;
		for(var i = 0; i < this.singleEvents.length; i++) {
			if (this.singleEvents[i].style.display == 'none'){
				this.singleEvents[i].removeAttribute('style');
				this.singleEvents[i].style.display = 'none'
			} else {
				this.singleEvents[i].removeAttribute('style');
			}
			var anchor = this.singleEvents[i].getElementsByTagName('a')[0];
			var start = getScheduleTimestamp(anchor.getAttribute('data-start')),
				duration = getScheduleTimestamp(anchor.getAttribute('data-end')) - start;

			var eventTop = slotHeight*(start - self.timelineStart)/self.timelineUnitDuration,
				eventHeight = slotHeight*duration/self.timelineUnitDuration;

            var f_size = (((eventHeight)%100)+20);
			if (f_size > 100){
				f_size = 100;
			}
			this.singleEvents[i].setAttribute('style', 'top: '+(eventTop-1)+'px; height: '+(eventHeight+1)+'px;' +' font-size: ' +(f_size)+'%;');
		}

		Util.removeClass(this.element, 'cd-schedule--loading');
	};

	ScheduleTemplate.prototype.initEvents = function() {
		var self = this;
		for(var i = 0; i < this.singleEvents.length; i++) {
			// open modal when user selects an event
			this.singleEvents[i].addEventListener('click', function(event){
				event.preventDefault();
				if(!self.animating) self.openModal(this.getElementsByTagName('a')[0]);
			});
		}
		//close modal window
		this.modalClose.addEventListener('click', function(event){
			event.preventDefault();
			if( !self.animating ) self.closeModal();
		});
		this.coverLayer.addEventListener('click', function(event){
			event.preventDefault();
			if( !self.animating ) self.closeModal();
		});
	};

	ScheduleTemplate.prototype.openModal = function(target) {
		var self = this;
		var mq = self.mq();
		this.animating = true;

		//update event name and time
		this.modalEventName.textContent = target.getElementsByTagName('em')[0].textContent;
		this.modalDate.textContent = target.getAttribute('data-start')+' - '+target.getAttribute('data-end');
		this.modal.setAttribute('data-event', target.getAttribute('data-event'));

		//update event content
		this.loadEventContent(target.getAttribute('data-content'));
		Util.addClass(this.modal, 'cd-schedule-modal--open');

		setTimeout(function(){
			//fixes a flash when an event is selected - desktop version only
			Util.addClass(target.closest('li'), 'cd-schedule__event--selected');
		}, 10);

		if( mq == 'mobile' ) {
			self.modal.addEventListener('transitionend', function cb(){
				self.animating = false;
				self.modal.removeEventListener('transitionend', cb);
			});
		} else {
			var eventPosition = target.getBoundingClientRect(),
				eventTop = eventPosition.top,
				eventLeft = eventPosition.left,
				eventHeight = target.offsetHeight,
				eventWidth = target.offsetWidth;

			var windowWidth = window.innerWidth,
				windowHeight = window.innerHeight;

			var modalWidth = ( windowWidth*.8 > self.modalMaxWidth ) ? self.modalMaxWidth : windowWidth*.8,
				modalHeight = ( windowHeight*.8 > self.modalMaxHeight ) ? self.modalMaxHeight : windowHeight*.8;

			var modalTranslateX = parseInt((windowWidth - modalWidth)/2 - eventLeft),
				modalTranslateY = parseInt((windowHeight - modalHeight)/2 - eventTop);

			var HeaderBgScaleY = modalHeight/eventHeight,
				BodyBgScaleX = (modalWidth - eventWidth);

			//change modal height/width and translate it
			self.modal.setAttribute('style', 'top:'+eventTop+'px;left:'+eventLeft+'px;height:'+modalHeight+'px;width:'+modalWidth+'px;transform: translateY('+modalTranslateY+'px) translateX('+modalTranslateX+'px)');
			//set modalHeader width
			self.modalHeader.setAttribute('style', 'width:'+eventWidth+'px');
			//set modalBody left margin
			self.modalBody.setAttribute('style', 'margin-left:'+eventWidth+'px');
			//change modalBodyBg height/width ans scale it
			self.modalBodyBg.setAttribute('style', 'height:'+eventHeight+'px; width: 1px; transform: scaleY('+HeaderBgScaleY+') scaleX('+BodyBgScaleX+')');
			//change modal modalHeaderBg height/width and scale it
			self.modalHeaderBg.setAttribute('style', 'height: '+eventHeight+'px; width: '+eventWidth+'px; transform: scaleY('+HeaderBgScaleY+')');

			self.modalHeaderBg.addEventListener('transitionend', function cb(){
				//wait for the  end of the modalHeaderBg transformation and show the modal content
				self.animating = false;
				Util.addClass(self.modal, 'cd-schedule-modal--animation-completed');
				self.modalHeaderBg.removeEventListener('transitionend', cb);
			});
		}

		//if browser do not support transitions -> no need to wait for the end of it
		this.animationFallback();
	};

	ScheduleTemplate.prototype.closeModal = function() {
		var self = this;
		var mq = self.mq();

		var item = self.element.getElementsByClassName('cd-schedule__event--selected')[0],
			target = item.getElementsByTagName('a')[0];

		this.animating = true;

		if( mq == 'mobile' ) {
			Util.removeClass(this.modal, 'cd-schedule-modal--open');
			self.modal.addEventListener('transitionend', function cb(){
				Util.removeClass(self.modal, 'cd-schedule-modal--content-loaded');
				Util.removeClass(item, 'cd-schedule__event--selected');
				self.animating = false;
				self.modal.removeEventListener('transitionend', cb);
			});
		} else {
			var eventPosition = target.getBoundingClientRect(),
				eventTop = eventPosition.top,
				eventLeft = eventPosition.left,
				eventHeight = target.offsetHeight,
				eventWidth = target.offsetWidth;

			var modalStyle = window.getComputedStyle(self.modal),
				modalTop = Number(modalStyle.getPropertyValue('top').replace('px', '')),
				modalLeft = Number(modalStyle.getPropertyValue('left').replace('px', ''));

			var modalTranslateX = eventLeft - modalLeft,
				modalTranslateY = eventTop - modalTop;

			Util.removeClass(this.modal, 'cd-schedule-modal--open cd-schedule-modal--animation-completed');

			//change modal width/height and translate it
			self.modal.style.width = eventWidth+'px';self.modal.style.height = eventHeight+'px';self.modal.style.transform = 'translateX('+modalTranslateX+'px) translateY('+modalTranslateY+'px)';
			//scale down modalBodyBg element
			self.modalBodyBg.style.transform = 'scaleX(0) scaleY(1)';
			//scale down modalHeaderBg element
			// self.modalHeaderBg.setAttribute('style', 'transform: scaleY(1)');
			self.modalHeaderBg.style.transform = 'scaleY(1)';

			self.modalHeaderBg.addEventListener('transitionend', function cb(){
				//wait for the  end of the modalHeaderBg transformation and reset modal style
				Util.addClass(self.modal, 'cd-schedule-modal--no-transition');
				setTimeout(function(){
					self.modal.removeAttribute('style');
					self.modalBody.removeAttribute('style');
					self.modalHeader.removeAttribute('style');
					self.modalHeaderBg.removeAttribute('style');
					self.modalBodyBg.removeAttribute('style');
				}, 10);
				setTimeout(function(){
					Util.removeClass(self.modal, 'cd-schedule-modal--no-transition');
				}, 20);
				self.animating = false;
				Util.removeClass(self.modal, 'cd-schedule-modal--content-loaded');
				Util.removeClass(item, 'cd-schedule__event--selected');
				self.modalHeaderBg.removeEventListener('transitionend', cb);
			});
		}

		//if browser do not support transitions -> no need to wait for the end of it
		this.animationFallback();
	};

	ScheduleTemplate.prototype.checkEventModal = function(modalOpen) {
		// this function is used on resize to reset events/modal style
		this.animating = true;
		var self = this;
		var mq = this.mq();
		if( mq == 'mobile' ) {
			//reset modal style on mobile
			self.modal.removeAttribute('style');
			self.modalBody.removeAttribute('style');
			self.modalHeader.removeAttribute('style');
			self.modalHeaderBg.removeAttribute('style');
			self.modalBodyBg.removeAttribute('style');
			Util.removeClass(self.modal, 'cd-schedule-modal--no-transition');
			self.animating = false;
		} else if( mq == 'desktop' && modalOpen) {
			Util.addClass(self.modal, 'cd-schedule-modal--no-transition cd-schedule-modal--animation-completed');
			var item = self.element.getElementsByClassName('cd-schedule__event--selected')[0],
				target = item.getElementsByTagName('a')[0];

			var eventPosition = target.getBoundingClientRect(),
				eventTop = eventPosition.top,
				eventLeft = eventPosition.left,
				eventHeight = target.offsetHeight,
				eventWidth = target.offsetWidth;

			var windowWidth = window.innerWidth,
				windowHeight = window.innerHeight;

			var modalWidth = ( windowWidth*.8 > self.modalMaxWidth ) ? self.modalMaxWidth : windowWidth*.8,
				modalHeight = ( windowHeight*.8 > self.modalMaxHeight ) ? self.modalMaxHeight : windowHeight*.8;

			var HeaderBgScaleY = modalHeight/eventHeight,
				BodyBgScaleX = (modalWidth - eventWidth);


			setTimeout(function(){
				self.modal.setAttribute('style', 'top:'+(windowHeight/2 - modalHeight/2)+'px;left:'+(windowWidth/2 - modalWidth/2)+'px;height:'+modalHeight+'px;width:'+modalWidth+'px;transform: translateY(0) translateX(0)');
				//change modal modalBodyBg height/width
				self.modalBodyBg.style.height = modalHeight+'px';self.modalBodyBg.style.transform = 'scaleY(1) scaleX('+BodyBgScaleX+')';self.modalBodyBg.style.width = '1px';
				//set modalHeader width
				self.modalHeader.setAttribute('style', 'width:'+eventWidth+'px');
				//set modalBody left margin
				self.modalBody.setAttribute('style', 'margin-left:'+eventWidth+'px');
				//change modal modalHeaderBg height/width and scale it
				self.modalHeaderBg.setAttribute('style', 'height: '+eventHeight+'px;width:'+eventWidth+'px; transform:scaleY('+HeaderBgScaleY+');');
			}, 10);

			setTimeout(function(){
				Util.removeClass(self.modal, 'cd-schedule-modal--no-transition');
				self.animating = false;
			}, 20);

		}
	};

	ScheduleTemplate.prototype.loadEventContent = function(content) {
		// load the content of an event when user selects it
		var self = this;

		httpRequest = new XMLHttpRequest();
		httpRequest.onreadystatechange = function() {
			if (httpRequest.readyState === XMLHttpRequest.DONE) {
	      if (httpRequest.status === 200) {
	      	self.modal.getElementsByClassName('cd-schedule-modal__event-info')[0].innerHTML = self.getEventContent(httpRequest.responseText);
	      	Util.addClass(self.modal, 'cd-schedule-modal--content-loaded');
	      }
	    }
		};
		httpRequest.open('GET', content+'.html');
    httpRequest.send();
	};

	ScheduleTemplate.prototype.getEventContent = function(string) {
		// reset the loaded event content so that it can be inserted in the modal
		var div = document.createElement('div');
		div.innerHTML = string.trim();
		return div.getElementsByClassName('cd-schedule-modal__event-info')[0].innerHTML;
	};

	ScheduleTemplate.prototype.animationFallback = function() {
		if( !this.supportAnimation ) { // fallback for browsers not supporting transitions
			var event = new CustomEvent('transitionend');
			self.modal.dispatchEvent(event);
			self.modalHeaderBg.dispatchEvent(event);
		}
	};

	ScheduleTemplate.prototype.mq = function(){
		//get MQ value ('desktop' or 'mobile')
		var self = this;
		return window.getComputedStyle(this.element, '::before').getPropertyValue('content').replace(/'|"/g, "");
	};

	function getScheduleTimestamp(time) {
		//accepts hh:mm format - convert hh:mm to timestamp
		time = time.replace(/ /g,'');
		if (time.includes(':')){
			var timeArray = time.split(':');
			var ap = timeArray[1].slice(-2);
			var difference = 0
			if (ap == 'pm' && parseInt(timeArray[0])!=12){
				difference = 720;
			}
			var timeStamp = parseInt(timeArray[0])*60 + parseInt(timeArray[1]) + difference;
		} else {
			var ap = time.slice(-2);
			var difference = 0
			if (ap == 'pm' && parseInt(time.slice(0,-2))!=12){
				difference = 720;
			}
			var timeStamp = parseInt(time.slice(0,-2))*60 + difference;
		}
		return timeStamp;
	};

	var scheduleTemplate = document.getElementsByClassName('js-cd-schedule'),
		scheduleTemplateArray = [],
		resizing = false;

	if( scheduleTemplate.length > 0 ) { // init ScheduleTemplate objects
		for( var i = 0; i < scheduleTemplate.length; i++) {
			(function(i){
				scheduleTemplateArray.push(new ScheduleTemplate(scheduleTemplate[i]));
			})(i);
		}

		window.addEventListener('resize', function(event) {
			// on resize - update events position and modal position (if open)
			if( !resizing ) {
				resizing = true;
				(!window.requestAnimationFrame) ? setTimeout(checkResize, 250) : window.requestAnimationFrame(checkResize);
			}
		});

		window.addEventListener('keyup', function(event){
			// close event modal when pressing escape key
			if( event.keyCode && event.keyCode == 27 || event.key && event.key.toLowerCase() == 'escape' ) {
				for(var i = 0; i < scheduleTemplateArray.length; i++) {
					scheduleTemplateArray[i].closeModal();
				}
			}
		});

		function checkResize(){
			for(var i = 0; i < scheduleTemplateArray.length; i++) {
				scheduleTemplateArray[i].scheduleReset();
			}
			resizing = false;
		};
	}

};
var count = 0;
var dict = {};

mainRun();
$('input[name="checkbox"]:checkbox').on('change', function() {
    var $this = $(this);
    var row = $this.closest('tr');
	var reload = true;
    if (this.checked){
        if (Object.keys(dict).length == 8){
            $(this).prop('checked', false);
            $("#myModal2").modal();
        } else {
            count++;
            count = count%9;
            if (count == 0) {
                count++;
            }
            $(this).closest('tr').each(function() {
                var cells = $('td', this);
                var visible = 0;
                var credits = $.trim(cells.eq(4).text().replace(" ",""));
                var id = cells.eq(0).text().replace(" ","");
                var trimmedmylist = $.trim('MYLIST'+cells.eq(0).text().replace(" ",""));
                var trimmedcrn = $.trim('CRN'+cells.eq(0).text().replace(" ",""));
                var crnnum =  $.trim(cells.eq(0).text().replace(" ",""));
                var meetingTimes = ((($.trim(cells.eq(2).text()).replace(/^\s*[\r\n]/gm, '')).replace(/\n+/g, ',')).replace(/\s+/g, '')).split(',');
                dict[(cells.eq(0).text().replace(/\s+/g, ''))] = [cells.eq(1).text(), meetingTimes, 1, credits, 0];

                var conflict = findConflicts(dict);
                var course_conflict = findDuplicateCourses(dict);
                var c = Object.values(conflict)
                var cc = Object.values(course_conflict)
                var c_keys = Object.keys(conflict)
                var cc_bool = true;
                var course_temp_name = (Object.values(dict[(id.replace(/\s+/g, ''))])[0])
                if (!($.isEmptyObject(course_conflict))){
                    for (var cond of cc){
                        for (var con of cond){
                            if (con.includes((id.replace(/\s+/g, '')))) {
                                cc_bool = false;
                            }
                        }
                    }
                }
                var c_bool = true;
                if (!($.isEmptyObject(conflict))){
                    for (var con of c_keys){
                        if ((conflict[con]).has(course_temp_name)) {
                            c_bool = false;
                        }
                    }
                }
                if (($.isEmptyObject(conflict) && $.isEmptyObject(course_conflict)) || (c_bool && cc_bool)){
                    $('#dataTable1').append('<tr><td style="width: 70%;">' + cells.eq(1).text() + '</td><td style="text-align: right;" class="custom-control custom-checkbox"><input class="custom-control-input" name="checkbox_mylist" type="checkbox" id="'+trimmedmylist+'" checked><label  class="custom-control-label" for="'+trimmedmylist+'"></label></td><td style="text-align: right; width: 15%;"><label style="font-size: 10px; margin-top: 4px;" class="switch"><input name="checkbox_alt" id="'+trimmedmylist+'1" type="checkbox"><span class="slider round"></span></label></td></tr>');
                    visible = 1
                    for(var i = 0; i < meetingTimes.length; i++) {
                        var daytime = meetingTimes[i].split(/:(.+)/);
                        var day = daytime[0];
                        var time = daytime[1].split('-');
                        var starttime = time[0]
                        var endtime = time[1]
                        var coursedata = (cells.eq(1).text()).split('-');
                        var course = coursedata[coursedata.length-2]+'-'+coursedata[coursedata.length-1];
                        $('#'+day).append('<li id="'+trimmedcrn+'" name="'+trimmedcrn+'" class="cd-schedule__event"><a data-start="'+starttime+'" data-end="'+endtime+'" data-content="" data-event="event-'+count.toString()+'" href="#0"><em class="cd-schedule__name">'+course+'</em></a></li>');
                    }
                 } else {
                    $('#mycoursesbody').append('<tr><td style="width: 70%;">' + cells.eq(1).text() + '</td><td style="text-align: right;" class="custom-control custom-checkbox"><input class="custom-control-input" name="checkbox_mylist" type="checkbox" id="'+trimmedmylist+'" ><label class="custom-control-label" for="'+trimmedmylist+'"></label></td><td style="text-align: right; width: 15%;"><label style="font-size: 10px; margin-top: 4px;" class="switch"><input name="checkbox_alt" id="'+trimmedmylist+'1" type="checkbox"><span class="slider round"></span></label></td></tr>');
                    visible = 0
                    dict[(id.replace(/\s+/g, ''))][2] = 0;
                    for(var i = 0; i < meetingTimes.length; i++) {
                        var daytime = meetingTimes[i].split(/:(.+)/);
                        var day = daytime[0];
                        var time = daytime[1].split('-');
                        var starttime = time[0]
                        var endtime = time[1]
                        var coursedata = (cells.eq(1).text()).split('-');
                        var course = coursedata[coursedata.length-2]+'-'+coursedata[coursedata.length-1];
                        $('#'+day).append('<li id="'+trimmedcrn+'" hidden="true" name="'+trimmedcrn+'" class="cd-schedule__event"><a data-start="'+starttime+'" data-end="'+endtime+'" data-content="" data-event="event-'+count.toString()+'" href="#0"><em class="cd-schedule__name">'+course+'</em></a></li>');
                    }
                 }
                 var myJSON = JSON.stringify({append: [crnnum, cells.eq(1).text(), meetingTimes, visible, credits, 0]});
                $.ajax({
                  type: 'POST',
                  url: 'http://localhost:5000/h_update',
                  // Always include an `X-Requested-With` header in every AJAX request,
                  // to protect against CSRF attacks.
                  headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                  },
                  contentType: 'application/octet-stream; charset=utf-8',
                  success: function(result) {
                  },
                  processData: false,
                  data: myJSON
                });
                mainRun(reload);
                row.insertBefore( row.parent().find('tr:first-child') );
            });
        };
    } else {
        $(this).closest('tr').each(function() {
            var cells = $('td', this);
            delete dict[(cells.eq(0).text().replace(/\s+/g, ''))];
            var id = cells.eq(0).text().replace(" ", "");
            $('#CRN'+id).remove();
            $('#MYLIST'+id).closest('tr').remove();
            var myJSON = JSON.stringify({remove: id});
            $.ajax({
              type: 'POST',
              url: 'http://localhost:5000/h_update',
              // Always include an `X-Requested-With` header in every AJAX request,
              // to protect against CSRF attacks.
              headers: {
                'X-Requested-With': 'XMLHttpRequest'
              },
              contentType: 'application/octet-stream; charset=utf-8',
              success: function(result) {
              },
              processData: false,
              data: myJSON
            });
			mainRun(reload);
            row.insertAfter( row.parent().find('tr:last-child') );
        });
    };
});

$(document).ready(function() {
    $('input[id^=select]').each(function() {
        $(this).trigger('click');
    });

    $('#mycoursesbody > tr').each(function() {
        var CRN = (($(this).find("input[name='checkbox_mylist']")).attr('id')).replace('MYLIST','');
        if (CRN in courseData_session){
            if ((courseData_session[CRN][2] == 0) && (($(this).find("input[name='checkbox_mylist']")).prop("checked") == true)){
                ($(this).find("input[name='checkbox_mylist']")).trigger('click');
            }
            if ((courseData_session[CRN][4] == 1)){
                ($(this).find("input[name='checkbox_alt']")).trigger('click');
            }
        }
    });
});

$('#mycoursesbody').on('change', 'input', function() {

    var $this = $(this);
	var id = this.id.replace(/\D/g,'');;
    if (this.checked){
        if (this.name == "checkbox_alt"){
            var selected_array = []
            for (var entry of Object.keys(dict)){
                if (dict[entry][4] == 1){
                    selected_array.push(dict[entry]);
                }
            }
            if (selected_array.length >= 6){
                $(this).prop('checked', false);
                $("#myModal_alt").modal();
            } else {
                id = id.slice(0, -1);
                dict[(id.replace(/\s+/g, ''))][4] = 1;
                var myJSON = JSON.stringify({update_alt: [id, 1]});
                $.ajax({
                      type: 'POST',
                      url: 'http://localhost:5000/h_update',
                      // Always include an `X-Requested-With` header in every AJAX request,
                      // to protect against CSRF attacks.
                      headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                      },
                      contentType: 'application/octet-stream; charset=utf-8',
                      success: function(result) {
                      },
                      processData: false,
                      data: myJSON
                    });
            }
        }
        else{
            dict[(id.replace(/\s+/g, ''))][2] = 1;
            var conflict = findConflicts(dict);
            var course_conflict = findDuplicateCourses(dict);

            var c = Object.values(conflict)
            var cc = Object.values(course_conflict)
            var c_keys = Object.keys(conflict)
            var cc_bool = true;
            var course_temp_name = (Object.values(dict[(id.replace(/\s+/g, ''))])[0])
            if (!($.isEmptyObject(course_conflict))){
                for (var con of cc){
                    if (con.includes(id)) {
                        cc_bool = false;
                    }
                }
            }
            var c_bool = true;
            if (!($.isEmptyObject(conflict))){
                for (var con of c_keys){
                    if ((conflict[con]).has(course_temp_name)) {
                        c_bool = false;
                    }
                }
            }
            if (($.isEmptyObject(conflict) && $.isEmptyObject(course_conflict)) || (c_bool && cc_bool)){
                var attr = $('li[name="CRN'+id+'"]').attr('hidden');
                if (typeof attr !== typeof undefined && attr !== false) {
                    $('li[name="CRN'+id+'"]').removeAttr('hidden');
                }
                var myJSON = JSON.stringify({update: [id, 1]});
                $.ajax({
                      type: 'POST',
                      url: 'http://localhost:5000/h_update',
                      // Always include an `X-Requested-With` header in every AJAX request,
                      // to protect against CSRF attacks.
                      headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                      },
                      contentType: 'application/octet-stream; charset=utf-8',
                      success: function(result) {
                      },
                      processData: false,
                      data: myJSON
                    });
                $('li[name="CRN'+id+'"]').show(500);
            } else {
                if (this.checked){
                    that = this;
                    switched = -1;
                    if ($.isEmptyObject(course_conflict)){
                        switched = 1;
                    }
                    else {
                        switched = 0;
                    };
                    var myJSON = JSON.stringify({update: [id, 0]});
                    $.ajax({
                      type: 'POST',
                      url: 'http://localhost:5000/h_update',
                      // Always include an `X-Requested-With` header in every AJAX request,
                      // to protect against CSRF attacks.
                      headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                      },
                      contentType: 'application/octet-stream; charset=utf-8',
                      success: function(result) {
                        $(that).trigger('click');
                      },
                      processData: false,
                      data: myJSON
                    });
                    if (switched == 1){
                        var days = "";
                        var courses = [];
                        for (var day in conflict){
                            days += day;
                        }
                        conflict[days[0]].forEach(element => courses.push(element));
                        $("#modalData").html('Course cannot be displayed because of time conflict on weekday(s): <b>' + days + '</b><br><br>Between the courses:<br><b>' + courses[0] + '</b><br><b>' + courses[1] + '</b>');
                        $("#myModal").modal();
                        dict[(id.replace(/\s+/g, ''))][2] = 0;
                    }
                    else if (switched == 0) {
                        var course_selected = (Object.values(dict[(id.replace(/\s+/g, ''))])[0]).split("-")
                        $("#modalData2").html('Course cannot be displayed because you have already selected this course with different section: <br><br><b>' + course_selected[0]+' - '+course_selected[1] + '</b>');
                        $("#myModal3").modal();
                        dict[(id.replace(/\s+/g, ''))][2] = 0;
                    }
                };

            };
        }

	} else {
	    if (this.name == "checkbox_alt"){
            id = id.slice(0, -1);
            dict[(id.replace(/\s+/g, ''))][4] = 0;
            var myJSON = JSON.stringify({update_alt: [id, 0]});
            $.ajax({
                  type: 'POST',
                  url: 'http://localhost:5000/h_update',
                  // Always include an `X-Requested-With` header in every AJAX request,
                  // to protect against CSRF attacks.
                  headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                  },
                  contentType: 'application/octet-stream; charset=utf-8',
                  success: function(result) {
                  },
                  processData: false,
                  data: myJSON
                });
        }
        else{
            dict[(id.replace(/\s+/g, ''))][2] = 0;
            var myJSON = JSON.stringify({update: [id, 0]});
                $.ajax({
                      type: 'POST',
                      url: 'http://localhost:5000/h_update',
                      // Always include an `X-Requested-With` header in every AJAX request,
                      // to protect against CSRF attacks.
                      headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                      },
                      contentType: 'application/octet-stream; charset=utf-8',
                      success: function(result) {
                      },
                      processData: false,
                      data: myJSON
                    });
            $('li[name="CRN'+id+'"]').hide(500, function(){
                $('li[name="CRN'+id+'"]').attr("hidden","true");
            });
        }

	};
    console.log(dict)
});

$("#saveSchedule").click(function() {
  $("#listdata").attr("value", JSON.stringify(dict));
  $("#savingbuttoncss").click();
});

// Convert String time to int time in military format
function convertTime(time){
  var isPM = (time.includes("pm"));
  var [hour, minute] = time.split(':');
  minute = minute.split(' ')[0];

  if (isPM && parseInt(hour) >= 1 && parseInt(hour) != 12) {
    hour = parseInt(hour) + 12;
  } else if (!isPM && parseInt(hour) == 12) {
    hour = 0;
  }

  hour = hour.toString();
  convertedTime = parseInt(hour + minute);

  return convertedTime;
}


// Find conflicts from a Dictionary of courses and time
// Returns dictionary of Days and their conflicting courses

// Following Format Assumed: {"12345": ["How to Make a Nuclear Bomb - CMPT 399 - 02",["T:9:20am-10:35am","R:9:20am-10:35am","F:3:00pm-5:00pm"]]}

function findConflicts(courses) {

  var conflictDict = {};
  var weekdaySchedule = {};

  // Iterate through dictionary
  for (let crn in courses) {
    var courseInfo = courses[crn];

    var courseName = courseInfo[0];
    var courseDaysAndTimes = courseInfo[1];
    if (courseInfo[2] != 0){
      // Iterate through class times
      for (s of courseDaysAndTimes) {
        day = s[0];
        timeInterval = s.slice(2);
        var [startTime, endTime] = timeInterval.split('-');
        startTime = convertTime(startTime);
        endTime = convertTime(endTime);

        // Add course info to dictionary
        if (day in weekdaySchedule) {
          weekdaySchedule[day].push([startTime, endTime, courseName]);
        } else {
          weekdaySchedule[day] = [[startTime, endTime, courseName]];
        }
      }
    }

  }

  // Loop through days and check for conflicts
  for (var [day, times] of Object.entries(weekdaySchedule)) {

    times.sort((a, b) => a[0] - b[0]); // Sort course by start times

    for (i = 1; i < times.length; i++) {
      startTime = times[i][0];
      lastEndTime = times[i - 1][1];

      if (startTime < lastEndTime) {
        conflictingClass1 = times[i - 1][2];
        conflictingClass2 = times[i][2];

        // Add conflicting courses to conflictDict
        if (day in conflictDict) {
          conflictDict[day].add(conflictingClass1);
          conflictDict[day].add(conflictingClass2);
        } else {
          conflictDict[day] = new Set();
          conflictDict[day].add(conflictingClass1);
          conflictDict[day].add(conflictingClass2);
        }
      }
    }
  }
  return conflictDict;
}

function findDuplicateCourses(courses) {

  var courseCounts = {};

  /*
  Loop to count the number of occurences for each course (adds to dictionary)

  Format: courseCounts[TITLE & COURSE NUMBER] = [COUNT, [CRNs]]
  */

  for (let crn in courses) {

    var courseInfo = courses[crn];
    var courseTitle = courseInfo[0];
    courseTitle = courseTitle.split(" - ", 2);
    var key = courseTitle[0] + " - " + courseTitle[1];
    if (courseInfo[2] != 0){
        if (key in courseCounts) {
          courseCounts[key][0] += 1;
          courseCounts[key][1].push(crn);
        } else {
          courseCounts[key] = [1, [crn]];
        }
    }
  }
  /*
  Add courses to Duplicate dictionary of count is greater than 1.
  Format: duplicates[TITLE & COURSE NUMBER] = [CRN's]
   */
  var duplicates = {};
  for (var [title, crns] of Object.entries(courseCounts)) {

    var courseCount = crns[0];
    if (courseCount > 1) {
      duplicates[title] = crns[1];
    }
  }

  return duplicates;
}
