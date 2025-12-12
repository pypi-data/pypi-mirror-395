#! /usr/bin/env hy
"""
    tqwgp-parser.parser
    ~~~~~~~~~~~~~~~~~~~~~
    Parse the definitions of TWWGP quotes and invoices.
    :copyright: (c) 2017-2023 Yoan Tournade <yoan@ytotech.com>.
"""
(import os)
(import .utils *)
(import functools [reduce])

;; Data parsing and normalization.

(defn parse-all-prestations [prestations vat-rate options [section None]]
  """
  Parse all prestations, returning a flattened list of prestations (in all-prestations)
  and a list of sections.
  Prestation parsed refer to section by their id (title).
  Sections contain all their prestations.
  """
  (setv all-prestations [])
  (setv sections [])
  (for [prestation prestations] ((fn [prestation]
    (if (in "prestations" prestation)
      (do
        (setv section-prestations
          (get (parse-all-prestations (get prestation "prestations") vat-rate options prestation) 0))
        (.append sections (parse-section prestation section-prestations vat-rate options))
        (.extend all-prestations section-prestations))
      (.append all-prestations (parse-prestation prestation section options))
    )) prestation))
  #(all-prestations sections))

(defn apply-any-price-formula [price price-formula]
  (if (and
        (get-in price-formula ["enabled"] False)
        (string? price)
        (!= price "")
        (= (get price 0) "="))
    (eval (cut price 1 None))
    price))

(defn parse-prestation [prestation section options]
  (merge-dicts [
    (parse-dict-values prestation
      ["title"]
      ["price" "quantity" "description" "batch" "optional"])
    {
      "price" (apply-any-price-formula
        (get-default prestation "price" None)
        (get options "price_formula"))
      "total" (compute-price [prestation]
        :count-optional True
        :rounding-decimals (get options "rounding-decimals")
        :price-formula (get options "price_formula"))
      "quantity" (get-default prestation "quantity" 1)
      "section" (get-default (if (none? section) {} section) "title" None)
      "batch" (parse-batch (get-default prestation "batch" (get-default (if (none? section) {} section) "batch" None)))
      "optional" (get-default prestation "optional" (get-default (if (none? section) {} section) "optional" False))
    }]))

(defn parse-section [section prestations vat-rate options]
  (merge-dicts [
    (parse-dict-values section
      ["title" "prestations"]
      ["description" "batch"])
    {
      "prestations" prestations
      "price" (compute-price-vat prestations
        :count-optional False
        :vat-rate vat-rate
        :rounding-decimals (get options "rounding-decimals")
        :price-formula (get options "price_formula"))
      "optional_price" (compute-price-vat prestations
        :count-optional True
        :vat-rate vat-rate
        :rounding-decimals (get options "rounding-decimals")
        :price-formula (get options "price_formula"))
      ;; TODO Normalize batch here: only set if all section prestation has same batch
      ;; (alternative: set a list of batches).
      "batch" (parse-batch (get-default section "batch" None))
      "optional" (get-default section "optional" False)
    }]))

(defn compute-discount [amount discount-spec]
  (cond
    (or (none? discount-spec) (none? amount))
    None
    
    (= "percent" (get discount-spec "mode"))
    (simplest-numerical-format
      (* amount (/ (get discount-spec "value") 100)))
    
    True
    (get discount-spec "value")))

(defn compute-price
        [prestations
          [count-optional False] [rounding-decimals None]
          [price-formula {}]]
  """
  Parse price of a flattened list of prestations
  (actually any list with object containing a price property),
  with quantity support.
  """
  ;; Must accept (but ignore for total) None and string values.
  ;; Set to None if no price defined at all.
  (rounded-number
    (reduce
      (fn [total prestation]
        (setv price (apply-any-price-formula (get prestation "price") price-formula))
        (setv add-price (and (numeric? price) (or count-optional (not (get-default prestation "optional" False)))))
        (setv prestation-total (when (numeric? price) (* price (get-default prestation "quantity" 1))))
        (cond
          (and add-price (numeric? total))
            (+ total prestation-total)
          add-price
            prestation-total
          True
            total))
      prestations
      None)
    rounding-decimals))

(defn compute-vat [price vat-rate [rounding-decimals None]]
  """
  Compute VAT part on a numerical price.
  vat-rate is represented as an integer percent points value, for e.g. 20 for a 20 % VAT rate.
  """
  (rounded-number
    (simplest-numerical-format (* (/ vat-rate 100) price))
    rounding-decimals))

(defn compute-price-vat
      [prestations
        [count-optional False]
        [vat-rate None]
        [rounding-decimals None]
        [price-formula {}]
        [discount-spec None]]
  """
  Compute price, as an object including VAT component, total with VAT excluded, total with VAT included ;
  from a list of objects containing a price (numerical) property.
  """
  ;; TODO Handle price object in element list, taking total_vat_excl for the summation?
  (setv gross-vat-excl (compute-price prestations
    :count-optional count-optional
    :rounding-decimals rounding-decimals
    :price-formula price-formula))
  (setv discount-vat-excl (compute-discount gross-vat-excl discount-spec))
  (setv total-vat-excl
    (if (none? discount-vat-excl)
      gross-vat-excl
      (- gross-vat-excl discount-vat-excl)))
  (if (numeric? vat-rate)
    (do
      (setv vat (if (none? total-vat-excl) None (compute-vat total-vat-excl vat-rate
        :rounding-decimals rounding-decimals)))
      {
        "vat" vat
        "total_vat_incl" (if (none? total-vat-excl)
          None
          (rounded-number (+ total-vat-excl vat) rounding-decimals))
        "total_vat_excl" total-vat-excl
        "gross_vat_excl" gross-vat-excl
        "discount_vat_excl" discount-vat-excl
      }
    )
    {
      "vat" None
      "total_vat_incl" total-vat-excl
      "total_vat_excl" total-vat-excl
      "gross_vat_excl" gross-vat-excl
      "discount_vat_excl" discount-vat-excl
    }))

(defn parse-batch [batch]
  (if (none? batch)
    None
    (str batch)))


;; Data recomposition/derivation from previously parsed data.

(defn has-section? [prestation]
  (not (none? (get prestation "section"))))

(defn not-has-section? [prestation]
  (not (has-section? prestation)))

(defn has-optional-section? [prestation]
  (and
    (has-section? prestation)
    (get-default (get prestation "section") "optional" False)))

(defn has-batch? [prestation]
  (and (in "batch" prestation) (not (none? (get prestation "batch")))))

(defn is-optional? [prestation]
  (get prestation "optional"))

(defn recompose-prestations [sections all-prestations]
  "Recompose prestations: is equal to all sections and all non-section prestations."
  (+ [] sections (list (filter not-has-section? all-prestations))))

(defn recompose-batches [all-prestations]
  "Recompose batches"
  ;; Get all batch names.
  (defn unique-batch-names [prestation]
    (reduce (fn [batches prestation]
    (setv batch (get prestation "batch"))
    (when (and (not (none? batch)) (not (in batch batches)))
      (.append batches batch))
      batches) all-prestations []))
  ;; Get all prestations that match the name.
  (defn batch-prestations [batch-name all-prestations]
    (list (filter (fn [prestation]
      (= (get prestation "batch") batch-name)) all-prestations)))
  ;; map-batch: get batch prestations and derive price.
  (defn map-batch [batch-name]
    (setv prestations (batch-prestations batch-name all-prestations))
    {
      "name" batch-name
      "prestations" prestations
      "price" (compute-price prestations)
    })
  (list (map map-batch (unique-batch-names all-prestations))))

(defn recompose-optional-prestations [sections all-prestations]
  "Recompose optional prestations: is equal to all optional sections and all optional non-section prestations."
  #((list (filter (fn [prestation]
                    (and (is-optional? prestation) (not (has-optional-section? prestation))))
          all-prestations))
    (list (filter is-optional? sections))))

(defn get-file-extension [filename]
  (get (.splitext os.path filename) 1))

(defn parse-resource [resource]
  (if (.startswith resource "http")
    { "path" (+ "__logo" (get-file-extension resource)) "url" resource}
    { "path" resource "file" resource }))

(defn parse-logo [logo]
  (if (none? logo)
    None
    (parse-resource logo)))

(defn parse-sect [sect]
  (merge-dicts [
    (parse-dict-values sect
      ["name" "email"]
      ; TODO Allows to pass other metadata / properties.
      ["logo" "logo_tex"])
    {
      "logo" (parse-logo (get-default sect "logo" None))
    }]))

(defn parse-parser-options [definition]
  {"price_formula" {
    "enabled" (get-in definition ["options" "price_formula" "enabled"] False)
  }})

(defn parse-discount [definition]
  ;; Use two properties for discount: discount_amount and discount_rate?
  ;; -> (Prefered) Or one property can be a numerical (currency) amount
  ;; or a percentage (passed as a string like "5%")
  (setv discount-def (get-default definition "discount" None))
  (setv discount-spec
    (cond
      (dict? discount-def)
      discount-def

      (numeric? discount-def)
      {"mode" "amount"
        "value" discount-def}

      (and (string? discount-def) (.isnumeric (.strip discount-def "%")))
      {"mode" "percent"
      "value" (int (.strip discount-def "%"))}

      True
      None))
  (if
    (none? discount-spec)
    None
    (merge-dicts [
      discount-spec
      {
        "title" (get-default discount-spec "title" None)
      }
    ])))

(defn parse-quote [definition #** kwargs]
  """
  Parse and normalize a quote definition.
  """
  (setv options (merge-dicts [
    {
      "rounding-decimals" 2
    }
    kwargs
    (parse-parser-options definition)
  ]))
  (setv vat-rate (get-default definition "vat_rate" None))
  (setv discount-spec (parse-discount definition))
  (setv #(all-prestations sections)
    (parse-all-prestations (get definition "prestations") vat-rate options))
  (setv #(all-optional-prestations optional-sections)
    (recompose-optional-prestations sections all-prestations))
  (setv has-quantities (any (map (fn [prestation] (> (get prestation "quantity") 1)) all-prestations)))
  (merge-dicts [
    ;; TODO Make the validation of the input dict recursive.
    (parse-dict-values definition
      ["title" "date" "author" "place" "sect" "client" "legal" "object" "prestations"]
      ;; TODO Do a pass-through: do not restrict other values.
      ["context" "version" "definitions" "conditions" "documents" "display_project_reference"
      "vat_rate" "discount"])
    {
      "sect" (parse-sect (get definition "sect"))
      "vat_rate" vat_rate
      "price" (compute-price-vat all-prestations
        :vat-rate vat-rate
        :rounding-decimals (get options "rounding-decimals")
        :price-formula (get options "price_formula")
        :discount-spec discount-spec)
      "discount" discount-spec
      ;; Derive sections from all-prestations (and sections too).
      "batches" (recompose-batches all-prestations)
      "all_prestations" all-prestations
      "sections" sections
      ;; Derive from section and all_prestations.
      "has_quantities" has-quantities
      "prestations" (recompose-prestations sections all-prestations)
      "optional_prestations" all-optional-prestations
      "optional_sections" optional-sections
      "optional_price" (compute-price-vat all-optional-prestations
        :count-optional True
        :vat-rate vat-rate
        :rounding-decimals (get options "rounding-decimals")
        :price-formula (get options "price_formula"))
      "display_project_reference" (none-or-true? (get-default definition "display_project_reference" True))
    }]))

(defn parse-line [line options]
  (merge-dicts [
    (parse-dict-values line
      ["title" "price"]
      ["description" "quantity"])
    {
      "quantity" (get-default line "quantity" 1)
      "price" (apply-any-price-formula
        (get-default line "price" None)
        (get options "price_formula"))
      "total" (compute-price [line]
        :count-optional True
        :rounding-decimals (get options "rounding-decimals")
        :price-formula (get options "price_formula"))
    }
  ]))

;; TODO Create Factur-X XML metadata.
;; TODO Implement a tool to merge XML and PDF to a Factur-X format.
;; https://fnfe-mpe.org/factur-x/implementer-factur-x/
;; https://github.com/akretion/factur-x
(defn parse-invoice [invoice invoices options]
  (setv lines (list (map (fn [line] (parse-line line options)) (get invoice "lines"))))
  (setv has-quantities (any (map (fn [line] (> (get line "quantity") 1)) lines)))
  (setv common-values (pick-by (fn [key]
    (in key ["author" "sect" "client" "legal" "vat_rate" "display_project_reference"])) invoices))
  (setv merged-invoice (merge-dicts [
    ;; Insert common values.
    common-values
    ;; Override by invoice ones if present (not None).
    (filter-dict
      (parse-dict-values invoice
        ["number" "date" "lines"]
        ;; TODO Do a pass-through: do not restrict other values.
        ["author" "sect" "client" "legal" "closing_note" "title" "vat_rate" "display_project_reference"])
      (fn [value key]
        (or (not (none? value)) (not (in key common-values)))))
    ]))
  (merge-dicts [
    merged-invoice
    {
      "sect" (parse-sect (get merged-invoice "sect"))
      "lines" lines
      "has_quantities" has-quantities
      "vat_rate" (get merged-invoice "vat_rate")
      "price" (compute-price-vat lines
        :vat-rate (get merged-invoice "vat_rate")
        :rounding-decimals (get options "rounding-decimals")
        :price-formula (get options "price_formula"))
      "display_project_reference" (none-or-true? (get-default merged-invoice "display_project_reference" True))
    }]))

(defn parse-invoices [definition #** kwargs]
  """
  Parse and normalize invoices definition.
  """
  (setv options (merge-dicts [
    {
      "rounding-decimals" 2
    }
    kwargs
    (parse-parser-options definition)
  ]))
  (defn parse-invoice-closure [invoice]
    (parse-invoice invoice definition options))
  (parse-dict-values definition
    ["author" "sect" "client" "legal" "invoices"]
    [])
  (setv invoices (get definition "invoices"))
  {
    "invoices" (list (map parse-invoice-closure (if invoices invoices [])))
  })
