from enum import Enum

__NAMESPACE__ = "http://ns.editeur.org/onix/3.0/reference"


class List1(Enum):
    """
    Notification or update type.

    Attributes:
        VALUE_01: Early notification Use for a complete record issued
            earlier than approximately six months before publication
        VALUE_02: Advance notification (confirmed) Use for a complete
            record issued to confirm advance information approximately
            six months before publication; or for a complete record
            issued after that date and before information has been
            confirmed from the book-in-hand
        VALUE_03: Notification confirmed on publication Use for a
            complete record issued to confirm advance information at or
            just before actual publication date, usually from the book-
            in-hand, or for a complete record issued at any later date
        VALUE_04: Update (partial) In ONIX 3.0 or later only, use when
            sending a ‘block update’ record. A block update implies
            using the supplied block(s) to update the existing record
            for the product, replacing only the blocks included in the
            block update, and leaving other blocks unchanged – for
            example, replacing old information from Blocks 4 and 6 with
            the newly-received data while retaining information from
            Blocks 1–3, 5 and 7–8 untouched. In previous ONIX releases,
            and for ONIX 3.0 or later using other notification types,
            updating is by replacing the complete record with the newly-
            received data
        VALUE_05: Delete Use when sending an instruction to delete a
            record which was previously issued. Note that a Delete
            instruction should NOT be used when a product is cancelled,
            put out of print, or otherwise withdrawn from sale: this
            should be handled as a change of Publishing status, leaving
            the receiver to decide whether to retain or delete the
            record. A Delete instruction is used ONLY when there is a
            particular reason to withdraw a record completely, eg
            because it was issued in error
        VALUE_08: Notice of sale Notice of sale of a product, from one
            publisher to another: sent by the publisher disposing of the
            product
        VALUE_09: Notice of acquisition Notice of acquisition of a
            product, by one publisher from another: sent by the
            acquiring publisher
        VALUE_88: Test update (partial) Only for use in ONIX 3.0 or
            later. Record may be processed for test purposes, but data
            should be discarded when testing is complete. Sender must
            ensure the &lt;RecordReference&gt; matches a previously-sent
            Test record
        VALUE_89: Test record Record may be processed for test purposes,
            but data should be discarded when testing is complete.
            Sender must ensure the &lt;RecordReference&gt; does not
            match any previously-sent live product record
    """

    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_08 = "08"
    VALUE_09 = "09"
    VALUE_88 = "88"
    VALUE_89 = "89"
