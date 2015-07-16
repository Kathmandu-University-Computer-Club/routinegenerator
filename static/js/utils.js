$(document).ready(function() {
	// $('form label input')
	// .after('<div class="underline"></div>')
	// .focus(function() {
	// 	var e = $(this);
	// 	e.closest('label').addClass('hasContent');
	// }).blur(function() {
	// 	var e = $(this);
	// 	e.closest('label')[e.val().length ? 'addClass' : 'removeClass']('hasContent');
	// });

	// $('button').mousedown(function() {
	// 	var t = $(this).addClass('active');
	// 	setTimeout(function() {
	// 		t.removeClass('active');
	// 	}, 1000);

	// });


	(function() {
		var pop = window.pop = {};
		
		(function() {
			var e_pw = $('#popupWrapper');
			var e_a = $('#alert');
			var e_btnOk = $('.btnOk', e_a);

			var clear = function() {
				pop.clear();
			};
	
			pop.alert = function(title, message, onOk, type) {
				$('.title', e_a).text(title);
				$('.message', e_a).text(message);
				e_a.removeClass("normal").removeClass("warn").addClass(type);
				e_btnOk.unbind("click");
				this.alert.onOk = onOk;
				e_btnOk.click(this.alert.onOk);
				e_pw.fadeIn();
				e_a.show();
				e_btnOk.click(clear).focus();
				setTimeout(function() {
					e_a.addClass('visible');
				}, 50);
			};
		})();

		pop.clear = function() {
			$('.popup').removeClass('visible');
			$('#popupWrapper').fadeOut();
			setTimeout(function() {
				$('.popup').hide();
			}, 200);
		}
	})();

});