# write your program here
filename = input()

original_plasmid_strand = []
restriction_site_plasmid_strand = []
gfp_original_strand = []
gfp_restriction_sites = None

with open(filename) as f:
    original_plasmid_strand.append(f.readline().strip())
    restriction_site_plasmid_strand.append(f.readline().strip())
    gfp_original_strand.append(f.readline().strip())
    gfp_restriction_sites = (f.readline().strip().split())


def ligation(strand_start, gfp, strand_end):
    ligated = [strand_start, gfp, strand_end]
    final_sequence = "".join(ligated)
    complementary_final = opposite_strand(final_sequence)
    return final_sequence, complementary_final


def opposite_strand(strand):
    translated_strand = ""
    opposite_values = {
        "T": "A",
        "A": "T",
        "C": "G",
        "G": "C"
    }

    for i in range(len(strand)):
        translated_strand += opposite_values[strand[i]]
    return translated_strand


complementary_plasmid = opposite_strand(original_plasmid_strand[0])
complementary_gfp = opposite_strand(gfp_original_strand[0])


def gfp_cut(strand, restriction_sites):
    complementary_strand = opposite_strand(strand[0])
    complementary_site_one = opposite_strand(restriction_sites[0])
    complementary_site_two = opposite_strand(restriction_sites[1])
    first_cut_index = strand[0].index(restriction_sites[0])
    second_cut_index = strand[0].index(restriction_sites[1])
    cutted_original = strand[0][first_cut_index + 1:second_cut_index + 1]
    first_cut_comp_index = complementary_strand.index(complementary_site_one)
    second_cut_comp_index = complementary_strand.index(complementary_site_two)
    cutted_complementary = complementary_strand[first_cut_comp_index + len(complementary_site_one) - 1:second_cut_comp_index + len(complementary_site_two) - 1]
    return cutted_original


def plasmid_cut(original, complementary, restriction_site):
    restriction_complement = opposite_strand(restriction_site)
    original_cut = original.replace(restriction_site, f'{restriction_site[0]} {restriction_site[1:]}')
    complementary_cut = complementary.replace(restriction_complement, f'{restriction_complement[:-1]} '
                                                                f'{restriction_complement[-1]}')
    final_original_cut = original_cut.split()
    begin = final_original_cut[0]
    end = final_original_cut[1]
    return begin, end


def main():
    original_plasmid_cut_begin, original_plasmid_cut_end = plasmid_cut(original_plasmid_strand[0], complementary_plasmid, restriction_site_plasmid_strand[0])
    gfp_original_cut = gfp_cut(gfp_original_strand, gfp_restriction_sites)
    original_glowing, complementary_glowing = ligation(original_plasmid_cut_begin, gfp_original_cut, original_plasmid_cut_end)
    print(f'{original_glowing}\n{complementary_glowing}')


if __name__ == main():
    main()