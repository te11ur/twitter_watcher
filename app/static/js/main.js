function update(fields, form) {
	for(var field in fields) {
		var val = fields[field];
		val = ['false', 'False'].indexOf(val) >= 0 ? false : val;
		val = ['true', 'True'].indexOf(val) >= 0 ? true : val;
		var elm = $('[name="' + field +'"]', form);
		if(elm.is('select')) {
			elm.find('option').each(function () {
				if(val != false) {
					if(this.label == val) {
						this.selected = true;
						return false;
					}
				} else if (this.defaultSelected) {
					this.selected = true;
					return false;
				}
			});
		} else if(elm.is('input')) {
			val = val != false ? decodeURIComponent(val) : false;
			if(elm.attr('type') == 'checkbox') {
				val != false ? elm.attr('checked', 'checked') : elm.removeAttr('checked');
			} else {
				elm.val(val || '');
			}
		} else if(elm.is('textarea')) {
			val = val != false ? decodeURIComponent(val) : false;
			elm.val(val || '');
		}
	}
}


$(function() {

	$('.element_add').click(function(e) {
		add();
		return false;
	});

	$('.element_edit').click(function(e) {
		edit($(this).data('id'));
		return false;
	});

	$('.element_delete').click(function(e) {
		remove($(this).data('id'));
		return false;
	});

	$('.element_action').each(function(){
		var elm = $(this);
		var data = elm.data();
		if(!data.model) {
			return;
		}
		elm.click(function() {
			$.ajax({
				url: '/admin/run/' + data.model + '/' + data.id,
				method: 'GET',
				dataType: 'json',
				success: function(data, textStatus, jqXHR) {
					if(data) {
						if(data.error) {
							console.log(data.error);
						} else {
							console.log(data);
						}
					}
				}
			});
		}).show();
	});
});
