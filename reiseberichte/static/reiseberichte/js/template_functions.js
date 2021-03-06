jQuery(document).ready(function() {


/* ---------------- Main Navigation ----------------- */
	
	
	/* Search Form*/
	
	$('input.search-form').on('keyup',function(){
		
		$(this).attr('class', 'search-form active-search');
		
		var count;
		var timeToEnd = 1000;

		$('input.search-form').keydown(function(){

			clearTimeout(count);
		    
		    count = setTimeout(endCount, timeToEnd);

		});
		
	});
	
	function endCount(){
		
		$('input.search-form').attr('class','search-form');

	}
	
	
	/* Map */
	
	function map() {
		
		jQuery('#googlemaps').gMap({
			maptype: 'ROADMAP',
			scrollwheel: false,
			zoom: 13,
			markers: [
				{
					address: 'Los Angeles, United States', // Your Adress Here
					html: '',
					popup: false,
				}

			],

		});
		
	}
	
	$('.contact-toggle').mouseenter(function(){
		
		if( $('#contact').is(':visible') ) {
			
			//do nothing
			
		} else {
			
			$('#contact-fake').slideDown(100);
			
		}
		
	}).mouseleave(function(){
		
		$('#contact-fake').slideUp(100);
		
	});
	
	$('.contact-toggle').click(function(){
		
		$('#contact').slideToggle();
		
		map();
		
		return false;
		
	});
	
	$('#close-contact').click(function(){
		
		$('#contact').slideUp();
		
		return false;
				
	});
	

	/* Menu */
	(function() {

		var $mainNav    = $('#navigation').children('ul');

		$mainNav.on('mouseenter', 'li', function() {
			var $this    = $(this),
				$subMenu = $this.children('ul');
			if( $subMenu.length ) $this.addClass('hover');
			$subMenu.hide().stop(true, true).slideDown('fast');
		}).on('mouseleave', 'li', function() {
			$(this).removeClass('hover').children('ul').stop(true, true).slideUp('fast');
		});
		
	})();
	
	/* Responsive Menu */
	(function() {
		selectnav('nav', {
			label: 'Menu',
			nested: true,
			indent: '-'
		});
				
	})();

/* ------------------ Image Overlay ----------------- */

	$(document).ready(function () {
	  $('.picture a').hover(function () {
		$(this).find('.image-overlay-zoom, .image-overlay-link').stop().fadeTo('fast', 1);
	  },function () {
		$(this).find('.image-overlay-zoom, .image-overlay-link').stop().fadeTo('fast', 0);
	  });
	});


/* ------------------ Back To Top ------------------- */
	
	jQuery('#scroll-top-top a').click(function(){
		jQuery('html, body').animate({scrollTop:0}, 300); 
		return false; 
	}); 
	
/* ------------------- Accordion -------------------- */	

	(function() {

		var $container = $('.acc-container'),
			$trigger   = $('.acc-trigger');

		$container.hide();
		$trigger.first().addClass('active').next().show();

		var fullWidth = $container.outerWidth(true);
		$trigger.css('width', fullWidth);
		$container.css('width', fullWidth);
		
		$trigger.on('click', function(e) {
			if( $(this).next().is(':hidden') ) {
				$trigger.removeClass('active').next().slideUp(300);
				$(this).toggleClass('active').next().slideDown(300);
			}
			e.preventDefault();
		});

		$(window).on('resize', function() {
			fullWidth = $container.outerWidth(true)
			$trigger.css('width', $trigger.parent().width() );
			$container.css('width', $container.parent().width() );
		});

	})();
/* ------------------ Alert Boxes ------------------- */	

jQuery(document).ready(function()
{
	jQuery(document.body).pixusNotifications({
			speed: 300,
			animation: 'fadeAndSlide',
			hideBoxes: false
	});
});

(function()
{
	$.fn.pixusNotifications = function(options)
	{
		var defaults = {
			speed: 200,
			animation: 'fade',
			hideBoxes: false
		};
		
		var options = $.extend({}, defaults, options);
		
		return this.each(function()
		{
			var wrapper = $(this),
				notification = wrapper.find('.notification'),
				content = notification.find('p'),
				title = content.find('strong'),
				closeBtn = $('<a class="close" href="#"></a>');
			
			$(document.body).find('.notification').each(function(i)
			{
				var i = i+1;
				$(this).attr('id', 'notification_'+i);
			});
			
			notification.filter('.closeable').append(closeBtn);
			
			closeButton = notification.find('> .close');
			
			closeButton.click(function()
			{
				hideIt( $(this).parent() );
				return false;
			});			
			
			function hideIt(object)
			{
				switch(options.animation)
				{
					case 'fade': fadeIt(object);     break;
					case 'slide': slideIt(object);     break;
					case 'box': boxAnimIt(object);     break;
					case 'fadeAndSlide': fadeItSlideIt(object);     break;
					default: fadeItSlideIt(object);
				}
			};
			
			function fadeIt(object)
			{	object
				.fadeOut(options.speed);
			}			
			function slideIt(object)
			{	object
				.slideUp(options.speed);
			}			
			function fadeItSlideIt(object)
			{	object
				.fadeTo(options.speed, 0, function() { slideIt(object) } );
			}			
			function boxAnimIt(object)
			{	object
				.hide(options.speed);
			}
			
			if (options.hideBoxes){}
			
			else if (! options.hideBoxes)
			{
				notification.css({'display': 'block', 'visiblity': 'visible'});
			}
			
		});
	};
})();

/*----------------------------------------------------*/
/*	Tabs
/*----------------------------------------------------*/

	(function() {

		var $tabsNav    = $('.tabs-nav'),
			$tabsNavLis = $tabsNav.children('li'),
			$tabContent = $('.tab-content');

		$tabsNav.each(function() {
			var $this = $(this);

			$this.next().children('.tab-content').stop(true,true).hide()
												 .first().show();

			$this.children('li').first().addClass('active').stop(true,true).show();
		});

		$tabsNavLis.on('click', function(e) {
			var $this = $(this);

			$this.siblings().removeClass('active').end()
				 .addClass('active');
			
			$this.parent().next().children('.tab-content').stop(true,true).hide()
														  .siblings( $this.find('a').attr('href') ).fadeIn();

			e.preventDefault();
		});

	})();

	/* ----------------- Contact Form ------------------- */		

	(function() {
	var animateSpeed=100;
	var emailReg = /^[a-zA-Z0-9._-]+@([a-zA-Z0-9.-]+\.)+[a-zA-Z0-9.-]{2,4}$/;

		// Validating

		function validateName(name) {
			if (name.val()=='*') {name.addClass('validation-error',animateSpeed); return false;}
			else {name.removeClass('validation-error',animateSpeed); return true;}
		}

		function validateEmail(email,regex) {
			if (!regex.test(email.val())) {email.addClass('validation-error',animateSpeed); return false;}
			else {email.removeClass('validation-error',animateSpeed); return true;}
		}

		function validateMessage(message) {
			if (message.val()=='') {message.addClass('validation-error',animateSpeed); return false;}
			else {message.removeClass('validation-error',animateSpeed); return true;}
		}

		$('input[name=name]').blur(function(){validateName($(this));});
		$('input[name=email]').blur(function(){validateEmail($(this),emailReg); });
		$('textarea[name=message]').blur(function(){validateMessage($(this)); });

	})();


	$('#send').click(function(){

		$.post("contact.php", { 

			new_message: 1,
			name: $('input[name=name]').val(),
			message_email: $('input[name=email]').val(),
			message: $('textarea[name=message]').val()

		}, function(data) {

			if(data==1) {

				alert('Message was sent');

			} else {

				alert('Ooops something goes wrong, try one more time!');

			}

		});

	});


/* -------------------- Isotope --------------------- */

$('#wrapper').imagesLoaded(function() {
		var $container = $('#portfolio-wrapper');
				$select = $('#filters select');
				
		// initialize Isotope
		$container.isotope({
		  // options...
		  resizable: false, // disable normal resizing
		  // set columnWidth to a percentage of container width
		  masonry: { columnWidth: $container.width() / 12 }
		});

		// update columnWidth on window resize
		$(window).smartresize(function(){
		  $container.isotope({
			// update columnWidth to a percentage of container width
			masonry: { columnWidth: $container.width() / 12 }
		  });
		});
		
		
	  $container.isotope({
		itemSelector : '.portfolio-item'
	  });
	  
	$select.change(function() {
			var filters = $(this).val();
	
			$container.isotope({
				filter: filters
			});
		});
	  
	  var $optionSets = $('#filters .option-set'),
		  $optionLinks = $optionSets.find('a');

	  $optionLinks.click(function(){
		var $this = $(this);
		// don't proceed if already selected
		if ( $this.hasClass('selected') ) {
		  return false;
		}
		var $optionSet = $this.parents('.option-set');
		$optionSet.find('.selected').removeClass('selected');
		$this.addClass('selected');
  
		// make option object dynamically, i.e. { filter: '.my-filter-class' }
		var options = {},
			key = $optionSet.attr('data-option-key'),
			value = $this.attr('data-option-value');
		// parse 'false' as false boolean
		value = value === 'false' ? false : value;
		options[ key ] = value;
		if ( key === 'layoutMode' && typeof changeLayoutMode === 'function' ) {
		  // changes in layout modes need extra logic
		  changeLayoutMode( $this, options )
		} else {
		  // otherwise, apply new options
		  $container.isotope( options );
		}
		
		return false;
	  });
	});
});

/* ------------------ Back To Top ------------------- */

$(window).scroll(function(){
	
	var y = $(window).scrollTop();
	
	if (y > 200) {
		
		$('#scroll-top-top').fadeIn();
		
	} else {
		
		$('#scroll-top-top').fadeOut();
		
	}

});

jQuery(document).ready(function($)
{
	var header_h = 74;
	var menu_h = 0;
	var body_l = $("body").width();
	var speed = 500;
	var logo2_url = $("link[rel='alternate']").attr("href");
	var logo2_link = $("link[rel='start']").attr("href");
	
	var scroll_critical = 74;
	var window_y = 0;
	var menu_left_margin = 100;
	menu_left_margin = parseInt($("#navigation-wrapper").css("width")) - parseInt($("ul.menu").width());
	
	window_y = $(window).scrollTop();
	var $logo2_link = $("<a/>", {"href": logo2_link})
	var $logo2 = $("<img />", {"src" : logo2_url, "class" : "logo2"}).appendTo($logo2_link);
	
		
	if ( (window_y > scroll_critical) && !(is_touch_device()) ) header_transform();
	
	function is_touch_device() {
	  return !!('ontouchstart' in window);
	}
	
	function header_transform(){
		
		var wrapper_l = $("#wrapper").width();
				
		if (wrapper_l > 767) {

			window_y = $(window).scrollTop();

			if (window_y > scroll_critical) {
				
				if (!($("#navigation-wrapper").hasClass("fixed"))){
						$("#header").css("margin-bottom", header_h + "px");
						$("#navigation-wrapper").addClass("fixed").css("top", "0px");
						$logo2_link.fadeIn().appendTo("#navigation-wrapper");
						$("#navigation").animate({ marginLeft: "70px" },500, function(){
							$("#logo-small").fadeIn();
						});
				}

				
			} else {
				
				if (($("#navigation-wrapper").hasClass("fixed"))){
						$("#navigation-wrapper").removeClass("fixed");
						$("#header").css("margin-bottom", "");
						$("#logo-small").fadeOut(function(){
							$(this).hide();
							$("#navigation").animate({ marginLeft: "0px" },500);
						});
					
				}

			}
			
		} else {
			$(".contact-toggle").removeAttr("class","contact-toggle");
		}	
	
	}
	
	

	
	$(window).scroll(function(){
		if (!(is_touch_device())) header_transform();			

	})
	
});

jQuery(document).ready(function($){

	// Add Active Class To Current Link
	var get_url = window.location.pathname.split( '/' ); // get current URL
	var url = get_url.slice(-1)[0]
		
	if (url == 0) {
		
		$('#nav a[href="index.html"]').addClass('active');
		
	} else {
		
		$('#nav a[href="'+url+'"]').addClass('active');
		
	}
	
	var $activeUL = $('.active').closest('ul');
	/*
	Revise below condition that tests if .active is a submenu
	*/
	if($activeUL.attr('id') != 'nav') { //check if it is submenu
	    $activeUL
	        .parent() //This should return the li
	        .children('a') //The childrens are <a> and <ul>
	        .addClass('active'); //add class active to the a    
	}

});