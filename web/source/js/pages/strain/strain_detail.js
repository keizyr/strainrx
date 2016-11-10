'use strict';

W.ns('W.pages.strain');

W.pages.strain.StrainDetailPage = Class.extend({

    effectNames: W.common.Constants.effectNames,
    benefitNames: W.common.Constants.benefitNames,
    sideEffectNames: W.common.Constants.sideEffectNames,
    flavorsNames: W.common.Constants.flavors,

    ui: {
        $strainId: $('.strain-id')
    },

    init: function init() {
        var that = this;
        this.retrieveStrain(function (strain_data) {
            if (strain_data) {
                that.model = new W.common.Model(strain_data);
                that.renderStrainDetails();

                $(window).resize(function () {
                    that.recalculateSimilarStrainsSectionWidth();
                });
            }
        });
    },

    retrieveStrain: function retrieveStrain(success) {
        $.ajax({
            method: 'GET',
            url: '/api/v1/search/strain/{0}/details'.format(this.ui.$strainId.val()),
            success: function (data) {
                success(data);
            }
        });
    },

    renderStrainDetails: function renderStrainDetails() {
        var template = _.template($('#strain_details_page').html());
        $('.strain-detail-wrapper').append(template({
            'model': this.model.getData(),
            'abbreviateStrainName': abbreviateStrainName
        }));

        function abbreviateStrainName(strainName) {
            var words = strainName.split(' '),
                abbreviation = '';

            if (words && words.length == 1) {
                abbreviation = words[0].substr(0, 2);
            } else {
                for (var i = 0; i < words.length; i++) {
                    abbreviation += words[i].substr(0, 1).toUpperCase();
                }
            }

            return abbreviation;
        }

        this.populateEffects();
        this.populateBenefits();
        this.populateSideEffects();
        this.populateFlavors();

        this.initRating();
        this.strainFavoriteHover();
        this.strainFavoriteClick();

        this.uploadPhotoListener();
        this.buildLocationsMenu();
        this.recalculateSimilarStrainsSectionWidth();
    },

    recalculateSimilarStrainsSectionWidth: function recalculateSimilarStrainsSectionWidth() {
        var $inner = $('.similar-strains-wrapper'),
            $similar = $inner.find('.similar-wrapper'),
            maxWidth = 0;

        $.each($similar, function () {
            var width = $(this).width();
            if (width > maxWidth) {
                maxWidth = width;
            }
        });

        $inner.css("width", maxWidth * 1.25 * $similar.length); // 1.25 coefficient to include padding to the width
    },

    initRating: function initRating() {
        var $strainRatingStars = $('.strain-rating-stars'),
            value = $strainRatingStars.text();
        $strainRatingStars.rateYo({
            rating: value,
            readOnly: true,
            spacing: '1px',
            normalFill: '#aaa8a8', // $grey-light
            ratedFill: '#6bc331', // $avocado-green
            starWidth: '16px'
        });
    },

    strainFavoriteHover: function strainFavoriteHover() {
        var $strainLike = $('.strain-like');

        $strainLike.mouseenter(function () {
            var $el = $(this);
            if (!$el.hasClass('active')) {
                $el.removeClass('fa-heart-o');
                $el.addClass('fa-heart');
                $el.addClass('heart-active');
            }
        });

        $strainLike.mouseleave(function () {
            var $el = $(this);
            if (!$el.hasClass('active')) {
                $el.addClass('fa-heart-o');
                $el.removeClass('fa-heart');
                $el.removeClass('heart-active');
            }
        });
    },

    strainFavoriteClick: function strainFavoriteClick() {
        var that = this,
            $strainLike = $('.strain-like');

        $strainLike.on('click', function () {
            var $el = $(this);
            if ($el.hasClass('active')) {
                that.likeStrain({
                    like: false
                }, function () {
                    $el.addClass('fa-heart-o');
                    $el.removeClass('fa-heart');
                    $el.removeClass('heart-active');
                    $el.removeClass('active');
                });
            } else {
                that.likeStrain({
                    like: true
                }, function () {
                    $el.removeClass('fa-heart-o');
                    $el.addClass('fa-heart');
                    $el.addClass('heart-active');
                    $el.addClass('active');
                });
            }
        });
    },

    likeStrain: function likeStrain(data, successCallback) {
        $.ajax({
            method: 'POST',
            url: '/api/v1/search/strain/like',
            dataType: 'json',
            data: JSON.stringify(data),
            success: function () {
                if (successCallback) {
                    successCallback();
                }
            }
        });
    },

    populateEffects: function populateEffects() {
        var that = this,
            effectsToDisplay = [];

        $.each(this.model.get('strain').effects, function (name, value) {
            if (value > 0) {
                effectsToDisplay.push({
                    name: that.effectNames[name],
                    value: value
                });
            }
        });

        effectsToDisplay.sort(this.sortValues);
        $('.effects-region').append(this.effectHtml(effectsToDisplay));
    },

    populateBenefits: function populateBenefits() {
        var that = this,
            benefitsToDisplay = [];

        $.each(this.model.get('strain').benefits, function (name, value) {
            if (value > 0) {
                benefitsToDisplay.push({
                    name: that.benefitNames[name],
                    value: value
                });
            }
        });

        benefitsToDisplay.sort(this.sortValues);
        $('.benefits-region').append(this.effectHtml(benefitsToDisplay));
    },

    populateSideEffects: function populateSideEffects() {
        var that = this,
            sideEffectsToDisplay = [];

        $.each(this.model.get('strain').side_effects, function (name, value) {
            if (value > 0) {
                sideEffectsToDisplay.push({
                    name: that.sideEffectNames[name],
                    value: value
                });
            }
        });

        sideEffectsToDisplay.sort(this.sortValues);
        $('.side-effects-region').append(this.sideEffectHtml(sideEffectsToDisplay));
    },

    populateFlavors: function populateFlavors() {
        var that = this,
            flavorsToDisplay = [];

        $.each(this.model.get('strain').flavor, function (name, value) {
            if (value > 0) {
                var flavor = that.flavorsNames[name];
                flavorsToDisplay.push({
                    name: flavor.name,
                    img: '<img src="{0}{1}"/>'.format(STATIC_URL, flavor.image),
                    value: value
                });
            }
        });

        flavorsToDisplay.sort(this.sortValues);
        $('.flavors-region').append(this.flavorsHtml(flavorsToDisplay));
    },

    sortValues: function sortValues(el1, el2) {
        var aName = el1.name, bName = el2.name,
            aValue = el1.value, bValue = el2.value;
        return aValue > bValue ? -1 : aValue < bValue ? 1 : aName < bName ? -1 : aName > bName ? 1 : 0;
    },

    effectHtml: function effectHtml(toDisplay) {
        var template = _.template($('#strain_effects').html());
        return template({'effects': toDisplay});
    },

    sideEffectHtml: function sideEffectHtml(toDisplay) {
        var template = _.template($('#strain_side_effects').html());
        return template({'effects': toDisplay});
    },

    flavorsHtml: function flavorsHtml(toDisplay) {
        var template = _.template($('#strain_flavors').html());
        return template({'flavors': toDisplay});
    },

    uploadPhotoListener: function uploadPhotoListener() {
        var that = this;
        $('.add-photo-link').on('click', function (e) {
            e.preventDefault();
            W.common.Dialog($('.upload-image-dialog'));

            $('.image-upload-form').on('submit', function (e) {
                e.preventDefault();
                $('.loader').removeClass('hidden');
                $('.btn-upload-image-submit').addClass('hidden');

                var file = $('.upload-image')[0].files[0],
                    formData = new FormData();

                formData.append('file', file);
                formData.append('name', file.name);

                $.ajax({
                    type: 'POST',
                    url: '/api/v1/search/strain/{0}/image'.format(that.ui.$strainId.val()),
                    enctype: 'multipart/form-data',
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function () {
                        $('.loader').addClass('hidden');
                        $('.btn-upload-image-submit').removeClass('hidden');
                        $('.upload-image-dialog').dialog('close');
                    }
                });
            });
        });
    },

    buildLocationsMenu: function buildLocationsMenu() {
        var $menuExpander = $('.menu-expander'),
            $menuLocations = $('.locations'),
            $menuFilter = $('.filter-menu'),
            $menuLink = $('.menu-link'),
            $priceExpander = $('.price-expander');

        $menuExpander.on('click', function () {
            $menuLocations.toggleClass('hidden');
            $menuFilter.toggleClass('expanded');
        });

        $menuFilter.mouseleave(function () {
            $menuLocations.addClass('hidden');
            $menuFilter.removeClass('expanded');
        });

        $menuLink.on('click', function (e) {
            e.preventDefault();
            $menuFilter.removeClass('expanded');
            $menuLocations.addClass('hidden');
        });

        $priceExpander.on('click', function () {
            $('.prices-wrapper').toggleClass('hidden');
        });

        $('.prices-wrapper').mouseleave(function () {
            $(this).addClass('hidden');
        });

        $('.price').on('click', function () {
            $('.prices-wrapper').addClass('hidden');
            var priceType = $(this).attr('id');
            $('.price-value').each(function (index, $el) {
                var $price = $($el);
                if ($price.attr('id') === priceType) {
                    $price.addClass('active');
                } else {
                    $price.removeClass('active');
                }
            });
        });

        $('.dispensary-rating').each(function () {
            var $this = $(this),
                rating = $this.text();

            $this.rateYo({
                rating: rating,
                readOnly: true,
                spacing: '1px',
                normalFill: '#aaa8a8', // $grey-light
                ratedFill: '#6bc331', // $avocado-green
                starWidth: '16px'
            });
        });
    }
});
