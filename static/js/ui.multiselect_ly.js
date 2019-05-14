/*
 * jQuery UI Multiselect
 *
 * Authors:
 *  Michael Aufreiter (quasipartikel.at)
 *  Yanick Rochon (yanick.rochon[at]gmail[dot]com)
 * 
 * Dual licensed under the MIT (MIT-LICENSE.txt)
 * and GPL (GPL-LICENSE.txt) licenses.
 * 
 * http://www.quasipartikel.at/multiselect/
 *
 * 
 * Depends:
 *	ui.core.js
 *	ui.sortable.js
 *
 * Optional:
 * localization (http://plugins.jquery.com/project/localisation)
 * scrollTo (http://plugins.jquery.com/project/ScrollTo)
 * 
 * Todo:
 *  Make batch actions faster
 *  Implement dynamic insertion through remote calls
 */


(function($) {

$.widget("ui.multiselect", {
  options: {
		sortable: true,
		searchable: true,
		animated: 'fast',
		show: 'slideDown',
		hide: 'slideUp',
		isDouble: false,
		dividerLocation: 0.6,
		nodeComparator: function(node1,node2) {
			var text1 = node1.text(),
			    text2 = node2.text();
			return text1 == text2 ? 0 : (text1 < text2 ? -1 : 1);
		}
	},
	_create: function() {
		this.element.hide();
		this.id = this.element.attr("id");
		this.container = $('<div class="ui-multiselect ui-helper-clearfix ui-widget"></div>').insertAfter(this.element);
		this.count = 0; // number of currently selected options
		
//        this.availableContainer = $('<div class="available" style="float:right"></div>').appendTo(this.container);
//		this.availableActions = $('<div class="actions ui-widget-header ui-helper-clearfix"><input type="text" class="search empty ui-widget-content ui-corner-all"/><a href="#" class="add-all">'+$.ui.multiselect.locale.addAll+'</a></div>').appendTo(this.availableContainer);
//		this.availableList = $('<ul class="available connected-list"><li class="ui-helper-hidden-accessible"></li></ul>').bind('selectstart', function(){return false;}).appendTo(this.availableContainer);
       
       if(!this.options.isDouble){
            this.flag = undefined;
            this.availableContainer = $('<div class="available" style="float:right"></div>').appendTo(this.container);
            this.availableActions = $('<div class="actions ui-widget-header ui-helper-clearfix"><input type="text" class="search empty ui-widget-content ui-corner-all"/><a href="#" class="add-all">'+$.ui.multiselect.locale.addAll+'</a></div>').appendTo(this.availableContainer);
            this.availableList = $('<ul class="available connected-list"><li class="ui-helper-hidden-accessible"></li></ul>').bind('selectstart', function(){return false;}).appendTo(this.availableContainer);
		    this.selectedContainer = $('<div class="selected"></div>').appendTo(this.container);
		    this.selectedActions = $('<div class="actions ui-widget-header ui-helper-clearfix"><span class="count">0 '+$.ui.multiselect.locale.itemsCount+'</span><a href="#" class="remove-all">'+$.ui.multiselect.locale.removeAll+'</a></div>').appendTo(this.selectedContainer);
		    this.selectedList = $('<ul class="selected connected-list"><li class="ui-helper-hidden-accessible"></li></ul>').bind('selectstart', function(){return false;}).appendTo(this.selectedContainer);
            // set dimensions
            //this.container.width(this.element.width());
            this.selectedContainer.width(Math.floor(this.element.width()*this.options.dividerLocation)*1.1);
            this.availableContainer.width(Math.floor(this.element.width()*(1-this.options.dividerLocation)*1.4));
            this.container.width(this.selectedContainer.width() + this.availableContainer.width());

            // fix list height to match <option> depending on their individual header's heights
            //this.selectedList.height(Math.max(this.element.height()-this.selectedActions.height(),1));
            //this.availableList.height(Math.max(this.element.height()-this.availableActions.height(),1));
		    this.selectedList.height(300);
            this.availableList.height(300);
        }
        else{
            this.flag = false;
		    this.count_l = 0; // number of currently selected options
		    this.count_r = 0; // number of currently selected options
		    this.selectedContainer_l = $('<div class="selected left" style="float:left"></div>').appendTo(this.container);
            this.availableContainer = $('<div class="available" style="float:left"></div>').appendTo(this.container);
		    this.selectedContainer_r = $('<div class="selected right" style="float:left"></div>').appendTo(this.container);
		    this.selectedActions_l = $('<div class="actions ui-widget-header ui-helper-clearfix"><span class="count">0 '+$.ui.multiselect.locale.itemsCount+'</span><a href="#" class="remove-all">'+$.ui.multiselect.locale.removeAll+'</a></div>').appendTo(this.selectedContainer_l);
		    this.availableActions = $('<div class="actions ui-widget-header ui-helper-clearfix"><input type="text" class="search empty ui-widget-content ui-corner-all"/><a href="#" class="add-all">'+$.ui.multiselect.locale.addAll+'</a></div>').appendTo(this.availableContainer);
		    this.selectedActions_r = $('<div class="actions ui-widget-header ui-helper-clearfix"><span class="count">0 '+$.ui.multiselect.locale.itemsCount+'</span><a href="#" class="remove-all">'+$.ui.multiselect.locale.removeAll+'</a></div>').appendTo(this.selectedContainer_r);
		    this.selectedList_l = $('<ul id = "clusterservicedisknewdev_a" class="selected connected-list"><li class="ui-helper-hidden-accessible"></li></ul>').bind('selectstart', function(){return false;}).appendTo(this.selectedContainer_l);
		    this.availableList = $('<ul id="double" class="available connected-list"><li class="ui-helper-hidden-accessible"></li></ul>').bind('selectstart', function(){return false;}).appendTo(this.availableContainer);
		    this.selectedList_r = $('<ul id="clusterservicedisknewdev_b" class="selected connected-list"><li class="ui-helper-hidden-accessible"></li></ul>').bind('selectstart', function(){return false;}).appendTo(this.selectedContainer_r);
		    this.selectedContainer_l.width(this.element.width() * 1.1);
		    this.selectedContainer_r.width(this.element.width() * 1.1);
		    this.selectedList_l.height(300);
		    this.selectedList_r.height(300);
            // set dimensions
            this.container.width(this.element.width() * 3.3);
            this.availableContainer.width(this.element.width());
            this.availableList.height(300);
        }
		var that = this;

		
		if ( !this.options.animated ) {
			this.options.show = 'show';
			this.options.hide = 'hide';
		}
		
		// init lists
		this._populateLists(this.element.find('option'));
		
		// make selection sortable
		if (this.options.sortable) {
			this._getTargetList(this.flag).sortable({
				placeholder: 'ui-state-highlight',
				axis: 'y',
				update: function(event, ui) {
					// apply the new sort order to the original selectbox
					that._getTargetList(that.flag).find('li').each(function() {
						if ($(this).data('optionLink'))
							$(this).data('optionLink').remove().appendTo(that.element);
					});
				},
				receive: function(event, ui) {
					ui.item.data('optionLink').attr('selected', true);
					// increment count
                    if(this.flag == false && !this.options.isDouble){
					    that.count += 1;
                    }
                    else if(this.flag == false){
					    that.count_l += 1;
                    }
                    else{
					    that.count_r += 1;
                    }
					that._updateCount();
					// workaround, because there's no way to reference 
					// the new element, see http://dev.jqueryui.com/ticket/4303
					that._getTargetList(that.flag).children('.ui-draggable').each(function() {
						$(this).removeClass('ui-draggable');
						$(this).data('optionLink', ui.item.data('optionLink'));
						$(this).data('idx', ui.item.data('idx'));
						that._applyItemState($(this), true);
					});
			
					// workaround according to http://dev.jqueryui.com/ticket/4088
					setTimeout(function() { ui.item.remove(); }, 1);
				}
			});
		}
		
		// set up livesearch
		if (this.options.searchable) {
			this._registerSearchEvents(this.availableContainer.find('input.search'));
		} else {
			$('.search').hide();
		}
	    if(this.options.isDouble){
            // batch actions
            this.container.find(".remove-all").click(function() {
                that._populateLists(that.element.find('option').removeAttr('selected'));
                return false;
            });
            
            this.container.find(".add-all").click(function() {
                that._populateLists(that.element.find('option').attr('selected', 'selected'));
                return false;
            });
        }
        else{
            this.container.find(".remove-all").click(function() {
                that._populateLists(that.element.find('option').removeAttr('selected'));
                return false;
            });
            
            this.container.find(".add-all").click(function() {
                that._populateLists(that.element.find('option').attr('selected', 'selected'));
                return false;
            });
        }
	},
	destroy: function() {
		this.element.show();
		this.container.remove();

		$.Widget.prototype.destroy.apply(this, arguments);
	},
	_populateLists: function(options) {
        if(!this.options.isDouble){
		    this.selectedList.children('.ui-element').remove();
        }
        else{
		    this._getTargetList(this.flag).children('.ui-element').remove();
        }
		this.availableList.children('.ui-element').remove();
        if(this.flag == undefined){
            this.count = 0;
        }
        else if(this.flag == false){
            this.count_l = 0;
        }
        else{
            this.count_r = 0;
        }

		var that = this;
		var items = $(options.map(function(i) {
	        var item = that._getOptionNode(this).appendTo(this.selected ? that._getTargetList(that.flag) : that.availableList).show();
			if (this.selected) that.count += 1;
			that._applyItemState(item, this.selected);
			item.data('idx', i);
			return item[0];
    }));
		
		// update count
		this._updateCount();
  },
	_updateCount: function() {
        if(this.flag == undefined){
		    this.selectedContainer.find('span.count').text(this.count+" "+$.ui.multiselect.locale.itemsCount);
        }
        else if(this.flag == false){
            if(!this.options.isDouble){
		        this.selectedContainer.find('span.count').text(this.count+" "+$.ui.multiselect.locale.itemsCount);
            }
		    else{
                this._getTargetContainer(this.flag).find('span.count').text(this.count_l+" "+$.ui.multiselect.locale.itemsCount);
            }
        }
        else{
		    this._getTargetContainer(this.flag).find('span.count').text(this.count_r+" "+$.ui.multiselect.locale.itemsCount);
        }
	},
	_getOptionNode: function(option) {
        if(!option.selected){
            option = $(option);
            var node = $('<li class="ui-state-default ui-element" title="'+option.text()+'"><span class="ui-icon"/><a href="#" class="action"><span class="ui-corner-all ui-icon span_l" /></a>'+option.text()+'<a href="#" class="action"><span class="ui-corner-all ui-icon span_r"/></a></li>').hide();
        }
        else{
            option = $(option);
            var node = $('<li class="ui-state-default ui-element" title="'+option.text()+'">'+option.text()+'<a href="#" class="action"><span class="ui-corner-all ui-icon"/></a></li>').hide();
        }
        node.data('optionLink', option);
		return node;
	},
	// clones an item with associated data
	// didn't find a smarter away around this
	_cloneWithData: function(clonee) {
		var clone = clonee.clone();
		clone.data('optionLink', clonee.data('optionLink'));
		clone.data('idx', clonee.data('idx'));
		return clone;
	},
	_setSelected: function(item, selected, targetList) {
		item.data('optionLink').attr('selected', selected);

		if (selected) {
			var selectedItem = this._cloneWithData(item);
			item[this.options.hide](this.options.animated, function() { $(this).remove(); });
			selectedItem.appendTo(this._getTargetList(this.flag)).hide()[this.options.show](this.options.animated);
			
			this._applyItemState(selectedItem, true);
			return selectedItem;
		} else {
			
			// look for successor based on initial option index
			var items = this.availableList.find('li'), comparator = this.options.nodeComparator;
			var succ = null, i = item.data('idx'), direction = comparator(item, $(items[i]));

			// TODO: test needed for dynamic list populating
			if ( direction ) {
				while (i>=0 && i<items.length) {
					direction > 0 ? i++ : i--;
					if ( direction != comparator(item, $(items[i])) ) {
						// going up, go back one item down, otherwise leave as is
						succ = items[direction > 0 ? i : i+1];
						break;
					}
				}
			} else {
				succ = items[i];
			}
			
			var availableItem = this._cloneWithData(item);
			succ ? availableItem.insertBefore($(succ)) : availableItem.appendTo(this.availableList);
			item[this.options.hide](this.options.animated, function() { $(this).remove(); });
			availableItem.hide()[this.options.show](this.options.animated);
			
			this._applyItemState(availableItem, false);
			return availableItem;
		}
	},
	_applyItemState: function(item, selected) {
		if (selected) {
			if (this.options.sortable)
				item.children('span').addClass('ui-icon-arrowthick-2-n-s').removeClass('ui-helper-hidden').addClass('ui-icon');
			else
				item.children('span').removeClass('ui-icon-arrowthick-2-n-s').addClass('ui-helper-hidden').removeClass('ui-icon');
			item.find('a.action span').addClass('ui-icon-close').removeClass('ui-icon-circle-arrow-e');
			item.find('a.action span.span_l').removeClass('ui-icon').removeClass('ui-icon-close');
			this._registerRemoveEvents(item.find('a.action'));
			
		} else {
			item.children('span').removeClass('ui-icon-arrowthick-2-n-s').addClass('ui-helper-hidden').removeClass('ui-icon');
			item.find('a.action span.span_l').addClass('ui-icon-circle-arrow-w').addClass('ui-icon').removeClass('ui-icon-close');
			item.find('a.action span.span_r').addClass('ui-icon-circle-arrow-e').removeClass('ui-icon-close');
			this._registerAddEvents(item.find('a.action'));
		}
		this._registerHoverEvents(item);
	},
	// taken from John Resig's liveUpdate script
	_filter: function(list) {
		var input = $(this);
		var rows = list.children('li'),
			cache = rows.map(function(){
				
				return $(this).text().toLowerCase();
			});
		
		var term = $.trim(input.val().toLowerCase()), scores = [];
		
		if (!term) {
			rows.show();
		} else {
			rows.hide();

			cache.each(function(i) {
				if (this.indexOf(term)>-1) { scores.push(i); }
			});

			$.each(scores, function() {
				$(rows[this]).show();
			});
		}
	},
	_registerHoverEvents: function(elements) {
		elements.removeClass('ui-state-hover');
		elements.mouseover(function() {
			$(this).addClass('ui-state-hover');
		});
		elements.mouseout(function() {
			$(this).removeClass('ui-state-hover');
		});
	},
	_registerAddEvents: function(elements) {
		var that = this;
        if(!this.options.isDouble){
            $($(elements)[0]).find('span').click(function() {
                that.flag = $(this).hasClass('span'); //change targetList
                that._getTargetContainer(that.flag);
                var item = that._setSelected($(this).parent().parent(), that._getTargetList(that.flag));
                that.count += 1;
                that._updateCount();
                return false;
            });
        }
        else{
            $($(elements)[0]).find('span').click(function() {
                that.flag = $(this).hasClass('span_r'); //change targetList
                that._getTargetContainer(that.flag);
                var item = that._setSelected($(this).parent().parent(), that._getTargetList(that.flag));
                that.count_l += 1;
                that._updateCount();
                return false;
            });
            $($(elements)[1]).find('span').click(function() {
                that.flag = $(this).hasClass('span_r');
                that._getTargetContainer(that.flag);
                var item = that._setSelected($(this).parent().parent(), that._getTargetList(that.flag));
                that.count_r += 1;
                that._updateCount();
                return false;
            });
        }
		
		// make draggable
		if (this.options.sortable) {
  		elements.each(function() {
  			$(this).parent().draggable({
  	      connectToSortable: that._getTargetList(that.flag),
  				helper: function() {
  					var selectedItem = that._cloneWithData($(this)).width($(this).width() - 50);
  					selectedItem.width($(this).width());
  					return selectedItem;
  				},
  				appendTo: that.container,
  				containment: that.container,
  				revert: 'invalid'
  	    });
  		});		  
		}
	},
	_registerRemoveEvents: function(elements) {
		var that = this;
		elements.click(function() {
            that.flag = $(this).parent().parent().parent().hasClass('right') //change targetList
			that._setSelected($(this).parent(), false, that.avaliableList);
            if(!that.options.isDouble){
                that.count -= 1;
            }
            else if($(this).parent().parent().parent().hasClass('left')){
                that.count_l -= 1;
            }
            else if($(this).parent().parent().parent().hasClass('right')){
                that.count_r -= 1;
            }
			that._updateCount();
			return false;
		});
 	},
	_registerSearchEvents: function(input) {
		var that = this;

		input.focus(function() {
			$(this).addClass('ui-state-active');
		})
		.blur(function() {
			$(this).removeClass('ui-state-active');
		})
		.keypress(function(e) {
			if (e.keyCode == 13)
				return false;
		})
		.keyup(function() {
			that._filter.apply(this, [that.availableList]);
		});
	},
    _getTargetList: function(flag) {
        
        if(!this.options.isDouble){
            var targetList = this.selectedList;
        }
        else{
            if(flag){
                var targetList = this.selectedList_r;
            }
            else{
                var targetList = this.selectedList_l;
            }
        }
        return targetList;
    },
    _getTargetContainer: function(flag) {
        
        if(!this.options.isDouble){
            var targeContainer = this.selectedList;
        }
        else{
            if(flag){
                var targetContainer= this.selectedContainer_r;
            }
            else{
                var targetContainer= this.selectedContainer_l;
            }
        }
        return targetContainer;
    }                                          
});
		
$.extend($.ui.multiselect, {
	locale: {
		addAll:'添加所有',
		removeAll:'移除所有',
		itemsCount:'块硬盘已选择'
	}
});


})(jQuery);
