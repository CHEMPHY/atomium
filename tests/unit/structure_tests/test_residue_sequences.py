from unittest import TestCase
from unittest.mock import Mock, patch
from atomium.structures.chains import ResidueSequence
from atomium.structures.molecules import Residue
from atomium.structures.atoms import Atom
from atomium.structures.exceptions import SequenceConnectivityError

class ResidueSequenceTest(TestCase):

    def setUp(self):
        self.sequence = ResidueSequence()
        self.atom1, self.atom2 = Mock(Atom), Mock(Atom)
        self.atom3, self.atom4 = Mock(Atom), Mock(Atom)
        self.atom5, self.atom6 = Mock(Atom), Mock(Atom)
        self.atom7, self.atom8 = Mock(Atom), Mock(Atom)
        self.residue1, self.residue2 = Mock(Residue), Mock(Residue)
        self.residue3, self.residue4 = Mock(Residue), Mock(Residue)
        self.residue1.id = "A1"
        self.residue2.id = "A2"
        self.residue3.id = "A3"
        self.residue4.id = "A4"
        self.residue1.name = "TYR"
        self.residue2.name = "VAL"
        self.residue3.name = "TYR"
        self.residue4.name = "MET"
        self.residue1.next = self.residue2
        self.residue2.next = self.residue3
        self.residue3.next = self.residue4
        self.residue4.next = None
        self.residue1.previous = None
        self.residue2.previous = self.residue1
        self.residue3.previous = self.residue2
        self.residue4.previous = self.residue3
        self.atom1.residue = self.residue1
        self.atom2.residue = self.residue1
        self.atom3.residue = self.residue2
        self.atom4.residue = self.residue2
        self.atom5.residue = self.residue3
        self.atom6.residue = self.residue3
        self.atom7.residue = self.residue4
        self.atom8.residue = self.residue4
        self.sequence._atoms = set([
         self.atom1, self.atom2, self.atom3, self.atom4,
         self.atom5, self.atom6, self.atom7, self.atom8
        ])



class ResidueSequenceLenTests(ResidueSequenceTest):

    @patch("atomium.structures.chains.ResidueSequence.residues")
    def test_can_get_len(self, mock_residues):
        mock_residues.return_value = (
         self.residue1, self.residue2, self.residue3, self.residue4
        )
        self.assertEqual(len(self.sequence), 4)



class ResidueSequenceIterTests(ResidueSequenceTest):

    @patch("atomium.structures.chains.ResidueSequence.residues")
    def test_can_get_len(self, mock_residues):
        mock_residues.return_value = (self.residue1, self.residue2)
        for res, correct_res in zip(self.sequence, (self.residue1, self.residue2)):
            self.assertEqual(res, correct_res)



class ResidueSequenceIndexTests(ResidueSequenceTest):

    @patch("atomium.structures.chains.ResidueSequence.residues")
    def test_can_get_len(self, mock_residues):
        mock_residues.return_value = (self.residue1, self.residue2)
        self.assertEqual(self.sequence[0], self.residue1)
        self.assertEqual(self.sequence[1], self.residue2)
        self.assertEqual(self.sequence[-1], self.residue2)



class ResidueSequenceResiduesTests(ResidueSequenceTest):

    @patch("atomium.structures.chains.AtomicStructure.residues")
    def test_can_get_residues(self, mock_residues):
        mock_residues.return_value = set(
         (self.residue1, self.residue2, self.residue3, self.residue4)
        )
        self.assertEqual(
         self.sequence.residues(),
         (self.residue1, self.residue2, self.residue3, self.residue4)
        )


    @patch("atomium.structures.chains.AtomicStructure.residues")
    def test_can_get_residues_after_filter(self, mock_residues):
        mock_residues.return_value = set(
         (self.residue2, self.residue4)
        )
        self.assertEqual(
         self.sequence.residues(a="a", b="b"),
         (self.residue2, self.residue4)
        )
        mock_residues.assert_called_with(self.sequence, a="a", b="b")


    @patch("atomium.structures.chains.AtomicStructure.residues")
    def test_can_get_no_residues(self, mock_residues):
        mock_residues.return_value = set()
        self.assertEqual(self.sequence.residues(), ())



class ResidueSequenceCorrectCheckingTests(ResidueSequenceTest):

    def test_can_verify_conected_residues(self):
        self.sequence._atoms = set([self.atom1, self.atom2])
        self.assertTrue(ResidueSequence.verify(self.sequence))
        self.sequence._atoms = set([self.atom3, self.atom4])
        self.assertTrue(ResidueSequence.verify(self.sequence))
        self.sequence._atoms = set([self.atom5, self.atom6])
        self.assertTrue(ResidueSequence.verify(self.sequence))
        self.sequence._atoms = set([self.atom7, self.atom8])
        self.assertTrue(ResidueSequence.verify(self.sequence))
        self.sequence._atoms = set([
         self.atom1, self.atom2, self.atom3, self.atom4
        ])
        self.assertTrue(ResidueSequence.verify(self.sequence))
        self.sequence._atoms = set([
         self.atom3, self.atom4, self.atom5, self.atom6
        ])
        self.assertTrue(ResidueSequence.verify(self.sequence))
        self.sequence._atoms = set([
         self.atom5, self.atom6, self.atom7, self.atom8
        ])
        self.assertTrue(ResidueSequence.verify(self.sequence))


    def test_can_reject_unconnected_residues(self):
        self.sequence._atoms = set([
         self.atom3, self.atom4, self.atom7, self.atom8
        ])
        with self.assertRaises(SequenceConnectivityError):
            ResidueSequence.verify(self.sequence)


    def test_empty_sequences_pass(self):
        self.sequence._atoms = set()
        self.assertTrue(ResidueSequence.verify(self.sequence))



class ResidueSequenceLengthTests(ResidueSequenceTest):

    @patch("atomium.structures.chains.ResidueSequence.__len__")
    def test_can_get_len(self, mock_len):
        mock_len.return_value = 100
        self.assertEqual(self.sequence.length, 100)
