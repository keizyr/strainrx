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

    templates: {
        expandedLocation: _.template($('#strain_detail_available_location').html())
    },

    priceSort: 'asc',

    init: function init() {
        var that = this;
        this.name = 'StrainDetailPage';

        $(window).on('resize', _.debounce(function () {
            that.recalculateSimilarStrainsSectionWidth();
        }, 250));

        this.retrieveStrain(function (strain_data) {
            if (strain_data) {
                that.model = new W.common.Model(strain_data);
                that.preformatModel();
                that.renderStrainDetails();
            }
        });

        W.subscribe.apply(this);
    },

    _on_close_popup: function _on_close_popup() {
        $('.locations').addClass('hidden');
        $('.filter-menu').removeClass('expanded');
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

    preformatModel: function preformatModel() {
        if (this.model.get('strain_reviews')) {
            $.each(this.model.get('strain_reviews'), function (index, review) {
                var date = new Date(review.created_date),
                    year = date.getFullYear() - 2000,
                    month = date.getMonth() + 1,
                    day = date.getDate();

                review.review = review.review ? review.review : '(No review written)';
                review.created_date = '{0}/{1}/{2}'.format(month, day, year);
            });
        }
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

        this.retrieveAndRenderAlsoLikeStrains();

        this.populateEffects();
        this.populateBenefits();
        this.populateSideEffects();
        this.populateFlavors();

        this.initRatings();
        this.strainFavoriteHover();
        this.strainFavoriteClick();

        this.uploadPhotoListener();
        this.buildLocationsMenu();
        this.showRateStrainDialog();
        this.submitStrainReview();
        this.showAllReviews();

        new W.pages.strain.StrainReviewDialog({
            model: this.model
        });
    },

    retrieveAndRenderAlsoLikeStrains: function retrieveAndRenderAlsoLikeStrains() {
        var $alsoLikeWrapper = $('.similar-strains-wrapper');
        $alsoLikeWrapper.html(W.common.Constants.html.loader);

        $.ajax({
            method: 'GET',
            url: '/api/v1/search/strain/{0}/also_like'.format($('.strain-id').val()),
            success: function (data) {
                if (data && data.also_like_strains) {
                    var template = _.template($('#strain_detail_also_like_template').html());
                    $alsoLikeWrapper.html('');
                    $.each(data.also_like_strains, function (i, s) {
                        $alsoLikeWrapper.append(template({s: s}));
                    });
                } else {
                    $('.strain-similar').addClass('hidden');
                }

                setTimeout(function () {
                    $(window).trigger('resize');
                }, 500);
            }
        });

        // 500 ms to hide a default ajax loader spinner
        setTimeout(function () {
            $('#loading-spinner').hide();
        }, 500);
    },

    recalculateSimilarStrainsSectionWidth: function recalculateSimilarStrainsSectionWidth() {
        var $parent = $('.similar-strains-wrapper'),
            $parentWidth = $parent.outerWidth(true),
            $parentFirstHidden = $('.similar-wrapper.similar-hidden', $parent).first();

        while (this.getVisibleSimilarWidth($parent) > $parentWidth) {
            var last = $('.similar-wrapper.similar-visible', $parent).last();
            last.addClass('similar-hidden');
            last.removeClass('similar-visible');
            last.css('visibility', 'hidden');
            last.css('position', 'absolute');
        }

        var padding = parseInt($('.similar-wrapper.similar-visible', $parent).first().css('padding'), 10),
            newTotalWidth = this.getVisibleSimilarWidth($parent) + $parentFirstHidden.outerWidth(true) + (3 * padding);

        if ($parentFirstHidden && $parentWidth > newTotalWidth) {
            $parentFirstHidden.removeClass('similar-hidden');
            $parentFirstHidden.addClass('similar-visible');
            $parentFirstHidden.css('visibility', 'visible');
            $parentFirstHidden.css('position', 'relative');
        }
    },

    getVisibleSimilarWidth: function getVisibleSimilarWidth($parent) {
        var totalVisibleSimilarWidth = 0;
        $.each($parent.find('.similar-wrapper.similar-visible'), function () {
            var $el = $(this),
                padding = parseInt($el.css('padding'), 10);
            totalVisibleSimilarWidth += (2 * padding) + $el.outerWidth(true);
        });
        return totalVisibleSimilarWidth;
    },

    initRatings: function initRatings() {
        var that = this,
            $strainRatingStars = $('.strain-rating-stars'),
            value = $strainRatingStars.text();

        this.initRating($strainRatingStars, value);
        $.each(this.model.get('strain_reviews'), function (index, review) {
            that.initRating($('.rating-{0}'.format(review.id)), review.rating);
            that.changeReviewText($('.display-text-{0}'.format(review.id)));
        });
        this.expandReviewText();
    },

    initRating: function initRating($ratingSelector, rating) {
        W.common.Rating.readOnly($ratingSelector, {rating: rating !== 'Not Rated' ? rating : 0});
    },

    changeReviewText: function changeReviewText($review) {
        var reviewHeight = $review.height(),
            reviewText = $review.text(),
            fontSize = parseInt($review.css('font-size'), 10);

        if (reviewHeight / fontSize >= 2) {
            reviewText = reviewText.substr(0, 150) + '... <span class="expander">Review full review</span>';
            $review.html(reviewText);
        }
    },

    expandReviewText: function expandReviewText() {
        $('.expander').on('click', function () {
            var parent = $(this).parent().parent();
            parent.find('.display').addClass('hidden');
            parent.find('.full').removeClass('hidden');
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
        var that = this;
        $.ajax({
            method: 'POST',
            url: '/api/v1/search/strain/{0}/favorite'.format(that.ui.$strainId.val()),
            dataType: 'json',
            data: JSON.stringify(data),
            success: function () {
                if (successCallback) {
                    successCallback();
                }
            }
        });
    },

    buildEffectsToDisplay: function buildEffectsToDisplay(rawEffects, userCriteria, effectNames) {
        var effectsToDisplay = [];
        $.each(rawEffects, function (name, value) {
            if (value > 0) {
                var userCriteriaValue = 0, criteriaEffect = [];
                if (userCriteria && userCriteria !== 'skipped') {
                    criteriaEffect = _.filter(userCriteria, function (o) {
                        return name === o.name;
                    });

                    if (criteriaEffect.length > 0) {
                        userCriteriaValue = criteriaEffect[0].value;
                    }
                }

                effectsToDisplay.push({
                    name: effectNames[name],
                    value: value,
                    userCriteriaValue: userCriteriaValue,
                    initialName: name
                });
            }
        });
        effectsToDisplay.sort(this.sortValues);
        return effectsToDisplay;
    },

    populateEffects: function populateEffects() {
        var that = this,
            review = this.model.get('user_strain_review'),
            userCriteria = this.model.get('user_criteria') || {},
            effects = review ? review.effects : this.model.get('strain').effects,
            toDisplay = this.buildEffectsToDisplay(effects, userCriteria.effects, this.effectNames),
            missingStrainEffects = [];

        if (userCriteria && userCriteria.effects && userCriteria.effects !== 'skipped') {
            $.each(userCriteria.effects, function (i, e) {
                var existsInStrain = _.filter(toDisplay, function (strainEffect) {
                    return strainEffect.initialName === e.name;
                });

                if (existsInStrain.length === 0) {
                    missingStrainEffects.push(e);
                }
            });
        }

        if (missingStrainEffects.length > 0) {
            $.each(missingStrainEffects, function (i, e) {
                if (e.value > 0) {
                    toDisplay.push({
                        name: that.effectNames[e.name],
                        value: e.value,
                        userCriteriaValue: e.value,
                        initialName: e.name,
                        missing: true
                    });
                }
            })
        }

        $('.effects-region').append(this.effectHtml(toDisplay));
    },

    populateBenefits: function populateBenefits() {
        var that = this,
            review = this.model.get('user_strain_review'),
            userCriteria = this.model.get('user_criteria') || {},
            effects = review ? review.benefits : this.model.get('strain').benefits,
            toDisplay = this.buildEffectsToDisplay(effects, userCriteria.benefits, this.benefitNames),
            missingStrainBenefits = [];

        if (userCriteria && userCriteria.benefits && userCriteria.benefits !== 'skipped') {
            $.each(userCriteria.benefits, function (i, e) {
                var existsInStrain = _.filter(toDisplay, function (strainEffect) {
                    return strainEffect.initialName === e.name;
                });

                if (existsInStrain.length === 0) {
                    missingStrainBenefits.push(e);
                }
            });
        }

        if (missingStrainBenefits.length > 0) {
            $.each(missingStrainBenefits, function (i, e) {
                if (e.value > 0) {
                    toDisplay.push({
                        name: that.benefitNames[e.name],
                        value: e.value,
                        userCriteriaValue: e.value,
                        initialName: e.name,
                        missing: true
                    });
                }
            })
        }

        $('.benefits-region').append(this.effectHtml(toDisplay));
    },

    populateSideEffects: function populateSideEffects() {
        var that = this,
            review = this.model.get('user_strain_review'),
            userCriteria = this.model.get('user_criteria') || {},
            effects = review ? review.side_effects : this.model.get('strain').side_effects,
            toDisplay = this.buildEffectsToDisplay(effects, userCriteria.side_effects, this.sideEffectNames),
            missingStrainSideEffects = [];

        if (userCriteria && userCriteria.side_effects && userCriteria.side_effects !== 'skipped') {
            $.each(userCriteria.side_effects, function (i, e) {
                var existsInStrain = _.filter(toDisplay, function (strainEffect) {
                    return strainEffect.initialName === e.name;
                });

                if (existsInStrain.length === 0) {
                    missingStrainSideEffects.push(e);
                }
            });
        }

        if (missingStrainSideEffects.length > 0) {
            $.each(missingStrainSideEffects, function (i, e) {
                if (e.value > 0) {
                    toDisplay.push({
                        name: that.sideEffectNames[e.name],
                        value: e.value,
                        userCriteriaValue: e.value,
                        initialName: e.name,
                        missing: true
                    });
                }
            })
        }

        $('.side-effects-region').append(this.sideEffectHtml(toDisplay));
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
        return template({
            'effects': toDisplay,
            'effectFillHtml': this.effectFillHtml,
            'userCriteriaFillHtml': this.userCriteriaFillHtml
        });
    },

    effectFillHtml: function effectFillHtml(effect) {
        var fillWidth = effect.value * 0.2 * 100, // 1 point should take 20% of parent width
            fillHtml = '<span class="{0}" style="width: {1}%"></span>';

        if (effect.missing) {
            fillHtml = fillHtml.format('', fillWidth);
        } else {
            fillHtml = fillHtml.format('fill', fillWidth);
        }

        return fillHtml;
    },

    userCriteriaFillHtml: function userCriteriaFillHtml(effect) {
        var fillWidth = (effect.userCriteriaValue >= 6 ? effect.userCriteriaValue - 5 : effect.userCriteriaValue) * 0.2 * 100, // 1 point should take 20% of parent width
            fillHtml = '<span class="{0}" style="{1}">{2}</span>',
            tearHtml = '<div class="tear"><span class="tear-value">{0}</span></div>'.format(effect.userCriteriaValue);

        if (fillWidth > 0) {
            if (effect.missing) {
                fillHtml = fillHtml.format('user-fill', 'width: {0}%'.format(fillWidth), tearHtml);
            } else {
                var strainValue = (effect.value >= 6 ? effect.value - 5 : effect.value) * 0.2 * 100;
                fillHtml = effect.userCriteriaValue > (effect.value >= 6 ? effect.value - 5 : effect.value) ?
                    fillHtml.format('user-fill', 'width: {0}%; left: {1}%'.format(fillWidth - strainValue, strainValue), tearHtml) :
                    fillHtml.format('user-fill', 'width: {0}%'.format(fillWidth), tearHtml);
            }
        } else {
            fillHtml = '';
        }

        return fillHtml;
    },

    sideEffectFillHtml: function sideEffectFillHtml(effect) {
        var fillWidth = (effect.value >= 6 ? effect.value - 5 : effect.value) * 0.2 * 100, // 1 point should take 20% of parent width
            fillHtml = '<span class="{0}" style="width: {1}%"></span>';

        if (effect.missing) {
            fillHtml = fillHtml.format('', fillWidth);
        } else {
            fillHtml = fillHtml.format('fill', fillWidth);
        }

        return fillHtml;
    },

    sideEffectHtml: function sideEffectHtml(toDisplay) {
        var template = _.template($('#strain_side_effects').html());
        return template({
            'effects': toDisplay,
            'sideEffectFillHtml': this.sideEffectFillHtml,
            'userCriteriaFillHtml': this.userCriteriaFillHtml
        });
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
                        $('.btn-upload-image-submit').addClass('hidden');
                        $('.submitted-message').removeClass('hidden');

                        var $btn = $('.btn-close');
                        $btn.removeClass('hidden');
                        $btn.on('click', function () {
                            $btn.addClass('hidden');
                            $('.btn-upload-image-submit').removeClass('hidden');
                            $('.photo-camera-wrapper').removeClass('hidden');
                            $('.preview-image-wrapper').addClass('hidden');
                            $('.submitted-message').addClass('hidden');
                            $('.upload-image-dialog').dialog('close');
                        });
                    }
                });
            });

            $('.upload-image').on('change', function (e) {
                e.preventDefault();
                var $el = $(this),
                    preview = $('.preview-image'),
                    file = $el[0].files[0],
                    reader = new FileReader();

                reader.addEventListener('load', function () {
                    $('.photo-camera-wrapper').addClass('hidden');
                    $('.preview-image-wrapper').removeClass('hidden');
                    $('.btn-upload-image-submit').removeAttr('disabled');
                    $('label[for="image-file"]').addClass('hidden');
                    preview[0].src = reader.result;
                }, false);

                if (file) {
                    reader.readAsDataURL(file);
                }
            });
        });
    },

    buildLocationsMenu: function buildLocationsMenu() {
        var that = this,
            $menuExpander = $('.active-link'),
            $menuLocations = $('.locations'),
            $menuFilter = $('.filter-menu'),
            menuTemplate = _.template($('#strain_detail_available_locations').html()),
            strainId = that.ui.$strainId.val();

        $menuExpander.on('click', function () {
            $menuLocations.toggleClass('hidden');
            $menuFilter.toggleClass('expanded');

            that.getDispensaries(function (dispensaries) {
                $menuLocations.html(menuTemplate({
                    dispensaries: dispensaries,
                    renderLocation: that.templates.expandedLocation,
                    formatDistance: that.formatDistance,
                    formatPrice: that.formatPrice,
                    strain_id: strainId
                }));

                $('.price-sort').on('click', function () {
                    $('.prices-wrapper').toggleClass('hidden');
                });

                $('.prices-wrapper').mouseleave(function () {
                    $(this).addClass('hidden');
                });

                $('.price').on('click', function () {
                    $('.prices-wrapper').addClass('hidden');
                    var priceType = $(this).attr('id');
                    that.sortByPrice(priceType, false);
                });

                $('.dispensary-rating').each(function () {
                    var $this = $(this);
                    if ($this.text() !== 'Not Rated') {
                        W.common.Rating.readOnly($this, {rating: $this.text()});
                    }
                });

                that.initSortActions();
            });
        });
    },

    renderLocation: function renderLocation(location) {
        var that = this;
        return this.templates.expandedLocation({
            d: location,
            formatDistance: this.formatDistance,
            formatPrice: this.formatPrice,
            strain_id: that.ui.$strainId.val()
        });
    },

    getDispensaries: function getDispensaries(success) {
        var that = this;
        if (this.locations) {
            success(this.locations);
        } else {
            $.ajax({
                method: 'GET',
                url: '/api/v1/search/strain/{0}/deliveries?filter=all&order_field=menu_items.price_gram&order_dir=asc'.format(this.ui.$strainId.val()),
                success: function (data) {
                    that.locations = data.locations;
                    success(data.locations);
                }
            });
        }
    },

    initSortActions: function initSortActions() {
        var that = this,
            $sort = $('.sort'),
            $priceSort = $('.price-expander');

        $sort.on('click', function () {
            var $this = $(this);
            that.sortBy($this, $this.attr('id'));
        });

        $priceSort.on('click', function () {
            that.sortByPrice($('.price-value.active').attr('id'), true);
        });
    },

    sortBy: function sortBy($sort, sortFieldName) {
        var that = this, newSort, url;

        this.changeSortArrow($sort);

        newSort = $sort.hasClass('fa-caret-up') ? 'desc' : 'asc';
        url = '/api/v1/search/strain/{0}/deliveries?filter={1}&order_field={2}&order_dir={3}'
            .format(this.ui.$strainId.val(), 'all', sortFieldName, newSort);

        $.ajax({
            method: 'GET',
            url: url,
            success: function (data) {
                if (data && data.locations) {
                    var $expandedHolder = $('.locations-area-body');
                    $expandedHolder.html('');

                    $.each(data.locations, function (i, l) {
                        $expandedHolder.append(that.renderLocation(l));
                    });

                    $.each($expandedHolder.find('.dispensary-rating'), function (i, el) {
                        var $ratingSelector = $(el);
                        that.initRating($ratingSelector, $ratingSelector.text());
                    });

                    $.each($('.price'), function () {
                        var $el = $(this);
                        if ($el.attr('id') === sortFieldName) {
                            $el.trigger('click');
                        }
                    });
                }
            }
        });
    },

    sortByPrice: function sortByPrice(sortFieldName, changeOrder) {
        var that = this, url;

        if (changeOrder) {
            this.priceSort = this.priceSort === 'asc' ? 'desc' : 'asc';
        }

        url = '/api/v1/search/strain/{0}/deliveries?filter={1}&order_field={2}&order_dir={3}'
            .format(this.ui.$strainId.val(), 'all', sortFieldName, this.priceSort);

        $.ajax({
            method: 'GET',
            url: url,
            success: function (data) {
                if (data && data.locations) {
                    var $expandedHolder = $('.locations-area-body');
                    $expandedHolder.html('');

                    $.each(data.locations, function (i, l) {
                        $expandedHolder.append(that.renderLocation(l));
                    });

                    $.each($expandedHolder.find('.dispensary-rating'), function (i, el) {
                        var $ratingSelector = $(el);
                        that.initRating($ratingSelector, $ratingSelector.text());
                    });

                    $('.price-value').each(function (index, $el) {
                        var $price = $($el);
                        if ($price.attr('id') === sortFieldName) {
                            $price.addClass('active');
                        } else {
                            $price.removeClass('active');
                        }
                    });
                }
            }
        });
    },

    changeSortArrow: function changeSortArrow($el) {
        if ($el.hasClass('fa-caret-down')) {
            $el.removeClass('fa-caret-down');
            $el.addClass('fa-caret-up');
        } else {
            $el.removeClass('fa-caret-up');
            $el.addClass('fa-caret-down');
        }
    },

    showRateStrainDialog: function showRateStrainDialog() {
        $('.rate-link').on('click', function (e) {
            e.preventDefault();
            W.common.RateDialog($('.rate-strain-dialog'));
        });
    },

    submitStrainReview: function submitStrainReview() {
        var that = this;
        $('.rate-strain-form').on('submit', function (e) {
            e.preventDefault();
            var rating = $('.rate-stars').rateYo('rating'),
                review = $('.rate-review').val();

            if (rating === 0) {
                $('.error-message').text('Rating is required');
                return;
            }

            if (review && review.length > 500) {
                $('.error-message').text('Review max length 500 is exceeded');
                return;
            }

            $('.loader').removeClass('hidden');
            $('.btn-review-submit').addClass('hidden');

            $.ajax({
                type: 'POST',
                url: '/api/v1/search/strain/{0}/rate'.format(that.ui.$strainId.val()),
                data: JSON.stringify({rating: rating, review: review}),
                success: function () {
                    $('.loader').addClass('hidden');
                    $('.btn-review-submit').removeClass('hidden');
                    $('.rate-stars').rateYo('rating', 0);
                    $('.review').val('');
                    $('.rate-strain-dialog').dialog('close');
                    window.location.reload();
                }
            });
        });
    },

    showAllReviews: function showAllReviews() {
        var that = this;
        $('.all-reviews-link-wrapper a').on('click', function (e) {
            e.preventDefault();
            $.ajax({
                method: 'GET',
                url: '/api/v1/search/strain/{0}/reviews'.format(that.ui.$strainId.val()),
                success: function (data) {
                    that.model.set('strain_reviews', data.reviews);
                    $('.all-reviews-link-wrapper').addClass('hidden');

                    var $reviewsRegion = $('.reviews-wrapper'),
                        reviewTemplate = _.template($('#strain_review_template').html());

                    $reviewsRegion.html('');
                    $.each(that.model.get('strain_reviews'), function (index, review) {
                        var date = new Date(review.created_date),
                            year = date.getFullYear() - 2000,
                            month = date.getMonth() + 1,
                            day = date.getDate();

                        review.review = review.review ? review.review : '(No review written)';
                        review.created_date = '{0}/{1}/{2}'.format(month, day, year);

                        $reviewsRegion.append(reviewTemplate({review: review}));
                        that.initRating($('.rating-{0}'.format(review.id)), review.rating);
                        that.changeReviewText($('.display-text-{0}'.format(review.id)));
                    });
                    that.expandReviewText();
                }
            });
        });
    },

    formatDistance: function formatDistance(d) {
        return d ? '({0}mi)'.format(Math.round(d * 100) / 100) : 'n/a';
    },

    formatPrice: function formatPrice(p) {
        return p ? '${0}'.format(p) : 'n/a';
    }
});
