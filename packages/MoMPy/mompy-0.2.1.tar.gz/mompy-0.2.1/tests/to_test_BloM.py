#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 15:04:31 2024

@author: carles
"""

nX = 2 # number of state preparations
nY = 1 # number of measurement settings
nB = 2 # number of measurement outcomes
nK = 1 # number of photon states (for avg photon numbe nK => n_trunc + 1

#---------------------------------------------------------------------#
#                        Collect all monomials                        #
#---------------------------------------------------------------------#

# Track operators in the tracial matrix
w_R = [] # Prepared quantum state
w_B = [] # Measurement
w_P = [] # Observable (photon number projector)

S_1 = [] # List of first order elements
cc = 1

for x in range(nX):
    S_1 += [cc]
    w_R += [cc]
    cc += 1

for y in range(nY):
    w_B += [[]]
    for b in range(nB):
        S_1 += [cc]
        w_B[y] += [cc]
        cc += 1
        
for k in range(nK):
    S_1 += [cc]
    w_P += [cc]
    cc += 1

# Additional higher order elements
S_high = [] # Some third order elements

# Second order elements
some_second = True
if some_second == True:
    for x in range(nX):
        for xx in range(nX):
            S_high += [[w_R[x],w_R[xx]]]
            
    for x in range(nX):
        for b in range(nB):
            for y in range(nY):
                S_high += [[w_R[x],w_B[y][b]]]
            
    for k in range(nK):
        for b in range(nB):
            for y in range(nY):
                S_high += [[w_P[k],w_B[y][b]]]
            
    for x in range(nX):
        for k in range(nK):
              S_high += [[w_P[k],w_R[x]]]

#S_high = []

# Set the operational rules within the SDP relaxation
list_states = [] # operators that do not commute with anything
rank_1_projectors = []
rank_1_projectors += w_R
rank_1_projectors += [w_B[y][b] for y in range(nY) for b in range(nB)]
rank_1_projectors += [w_P[k] for k in range(nK)]
orthogonal_projectors = []
orthogonal_projectors += [ w_B[y] for y in range(nY)]
orthogonal_projectors += [ w_P ] 
commuting_variables = [] # commuting elements (wxcept with elements in "list_states"
commuting_variables += [w_B[y][b] for y in range(nY) for b in range(nB)]
commuting_variables += w_P
commuting_variables += w_R

print('Rank-1 projectors',rank_1_projectors)
print('Orthogonal projectors',orthogonal_projectors)
print('commuting elements',commuting_variables)

[Block_Matrix,map_table,S,list_of_eq_indices,Mexp] = BlockMatrix(S_1,[],S_high,rank_1_projectors,orthogonal_projectors,commuting_variables,list_states)

print('Matrix size:',np.shape(Block_Matrix))

#print(fmap(map_table,[w_R[0],w_B[0][0],w_P[0]]))
#print(fmap(map_table,[w_R[0],w_P[0],w_B[0][0]]))

print(Block_Matrix)
#for element in map_table:
#    print(element)
