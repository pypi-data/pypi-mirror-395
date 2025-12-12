/*
 * Copyright 2025 NVIDIA Corporation.  All rights reserved.
 *
 * NOTICE TO LICENSEE:
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 *
 * These Licensed Deliverables contained herein is PROPRIETARY and
 * CONFIDENTIAL to NVIDIA and is being provided under the terms and
 * conditions of a form of NVIDIA software license agreement by and
 * between NVIDIA and Licensee ("License Agreement") or electronically
 * accepted by Licensee.  Notwithstanding any terms or conditions to
 * the contrary in the License Agreement, reproduction or disclosure
 * of the Licensed Deliverables to any third party without the express
 * written consent of NVIDIA is prohibited.
 *
 * NOTWITHSTANDING ANY TERMS OR CONDITIONS TO THE CONTRARY IN THE
 * LICENSE AGREEMENT, NVIDIA MAKES NO REPRESENTATION ABOUT THE
 * SUITABILITY OF THESE LICENSED DELIVERABLES FOR ANY PURPOSE.  IT IS
 * PROVIDED "AS IS" WITHOUT EXPRESS OR IMPLIED WARRANTY OF ANY KIND.
 * NVIDIA DISCLAIMS ALL WARRANTIES WITH REGARD TO THESE LICENSED
 * DELIVERABLES, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY,
 * NONINFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
 * NOTWITHSTANDING ANY TERMS OR CONDITIONS TO THE CONTRARY IN THE
 * LICENSE AGREEMENT, IN NO EVENT SHALL NVIDIA BE LIABLE FOR ANY
 * SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, OR ANY
 * DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
 * WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
 * ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
 * OF THESE LICENSED DELIVERABLES.
 *
 * U.S. Government End Users.  These Licensed Deliverables are a
 * "commercial item" as that term is defined at 48 C.F.R. 2.101 (OCT
 * 1995), consisting of "commercial computer software" and "commercial
 * computer software documentation" as such terms are used in 48
 * C.F.R. 12.212 (SEPT 1995) and is provided to the U.S. Government
 * only as a commercial end item.  Consistent with 48 C.F.R.12.212 and
 * 48 C.F.R. 227.7202-1 through 227.7202-4 (JUNE 1995), all
 * U.S. Government End Users acquire the Licensed Deliverables with
 * only those rights set forth herein.
 *
 * Any use of the Licensed Deliverables in individual and commercial
 * software must include, in the user documentation and internal
 * comments to the code, the above Disclaimer and U.S. Government End
 * Users Notice.
 */

#pragma once

#define CUTENSORMP_MAJOR 0
#define CUTENSORMP_MINOR 1
#define CUTENSORMP_PATCH 0
#define CUTENSORMP_VERSION (CUTENSORMP_MAJOR * 10000 + CUTENSORMP_MINOR * 100 + CUTENSORMP_PATCH)

#include <cutensor.h>
#include <nccl.h>

#include "cutensorMp/types.h"

#ifdef __cplusplus
extern "C"
{
#endif
    /**
     * \brief Initializes the cutensorMp library and creates a handle for distributed tensor operations.
     *
     * \details This function creates a cutensorMp handle that serves as the context for all
     * distributed tensor operations. The handle is associated with a specific MPI communicator,
     * local CUDA device, and CUDA stream. This allows cutensorMp to coordinate tensor operations
     * across multiple processes and GPUs.
     *
     * The communicator defines the group of processes that will participate in distributed
     * tensor operations. The local device ID specifies which CUDA device on the current
     * process will be used for computations. The CUDA stream enables asynchronous execution
     * and synchronization with other CUDA operations.
     *
     * The user is responsible for calling \ref cutensorMpDestroy to free the resources
     * associated with the handle.
     *
     * \param[out] handle Pointer to cutensorMpHandle_t that will hold the created handle
     * \param[in] comm NCCL communicator that defines the group of processes for distributed operations
     * \param[in] local_device_id CUDA device ID to use on the current process (must be valid and accessible)
     * \param[in] stream CUDA stream for asynchronous operations
     *
     * \retval CUTENSOR_STATUS_SUCCESS on success and an error code otherwise
     * \remarks non-blocking, no reentrant, and thread-safe
     */
    cutensorStatus_t cutensorMpCreate(cutensorMpHandle_t* handle, ncclComm_t comm, int local_device_id,
                                      cudaStream_t stream);

    /**
     * \brief Frees all resources associated with the provided cutensorMp handle.
     *
     * \details This function deallocates all memory and resources associated with a cutensorMp handle
     * that was previously created by \ref cutensorMpCreate. After calling this function, the handle
     * becomes invalid and should not be used in subsequent cutensorMp operations.
     *
     * \param[in,out] handle The cutensorMpHandle_t object that will be deallocated
     *
     * \retval CUTENSOR_STATUS_SUCCESS on success and an error code otherwise
     * \remarks blocking, no reentrant, and thread-safe
     */
    cutensorStatus_t cutensorMpDestroy(cutensorMpHandle_t handle);

    /**
     * \brief Creates a distributed tensor descriptor for multi-process tensor operations.
     *
     * \details This function creates a tensor descriptor that defines the structure and distribution
     * of a multi-dimensional tensor across multiple processes. Unlike regular cuTENSOR
     * tensor descriptors, this descriptor includes information about how the tensor is partitioned
     * and distributed across different processes in the MPI communicator.
     *
     * The tensor is described by its modes (dimensions), extents (sizes along each mode), and
     * strides for elements and blocks. The distribution is specified through block sizes, block
     * strides, and nranks-per-mode, which determine how the tensor data is partitioned across
     * the participating processes.
     *
     * The user is responsible for calling \ref cutensorMpDestroyTensorDescriptor to free the
     * resources associated with the descriptor once it is no longer needed.
     *
     * \param[in] handle Opaque handle holding cutensorMp's library context
     * \param[out] desc Pointer to the address where the allocated tensor descriptor object will be stored
     * \param[in] numModes Number of modes (dimensions) in the tensor (must be greater than zero)
     * \param[in] extent Extent (size) of each mode (size: numModes, all values must be greater than zero)
     * \param[in] elementStride Stride between consecutive elements in each mode (size: numModes)
     * \param[in] blockSize Size of each block along each mode for distribution (size: numModes), passing null will using extent[i]/nranksPerMode[i]
     * \param[in] blockStride Stride between consecutive blocks in each mode (size: numModes)
     * \param[in] nranksPerMode Number of processes along each mode (size: numModes)
     * \param[in] nranks Total number of ranks (processes) participating in the tensor distribution
     * \param[in] ranks Array of rank IDs for each participating process (size: nranks), passing null will use the range [0, nranks)
     * \param[in] dataType Data type of the tensor elements
     *
     * \retval CUTENSOR_STATUS_SUCCESS The operation completed successfully
     * \retval CUTENSOR_STATUS_NOT_INITIALIZED if the handle is not initialized
     * \retval CUTENSOR_STATUS_INVALID_VALUE if some input data is invalid (this typically indicates a user error)
     * \retval CUTENSOR_STATUS_NOT_SUPPORTED if the requested descriptor configuration is not supported
     * \remarks non-blocking, no reentrant, and thread-safe
     */
    cutensorStatus_t cutensorMpCreateTensorDescriptor(const cutensorMpHandle_t handle, cutensorMpTensorDescriptor_t* desc,
                                                      const uint32_t numModes, const int64_t extent[],
                                                      const int64_t elementStride[], const int64_t blockSize[],
                                                      const int64_t blockStride[], const int64_t nranksPerMode[],
                                                      const uint32_t nranks, const int32_t ranks[],
                                                      const cudaDataType_t dataType);

    /**
     * \brief Frees all resources related to the provided distributed tensor descriptor.
     *
     * \details This function deallocates all memory and resources associated with a cutensorMp
     * tensor descriptor that was previously created by \ref cutensorMpCreateTensorDescriptor.
     * After calling this function, the descriptor becomes invalid and should not be used in
     * subsequent cutensorMp operations.
     *
     * \param[in,out] desc The cutensorMpTensorDescriptor_t object that will be deallocated
     *
     * \retval CUTENSOR_STATUS_SUCCESS on success and an error code otherwise
     * \remarks blocking, no reentrant, and thread-safe
     */
    cutensorStatus_t cutensorMpDestroyTensorDescriptor(cutensorMpTensorDescriptor_t desc);

    /**
     * \brief Creates an operation descriptor that encodes a distributed tensor contraction.
     *
     * \details This function creates an operation descriptor for distributed tensor contractions
     * of the form \f$ D = \alpha \mathcal{A} \mathcal{B} + \beta \mathcal{C} \f$, where the tensors
     * A, B, C, and D are distributed across multiple processes as specified by their
     * respective tensor descriptors.
     *
     * The distributed contraction leverages both intra-process cuTENSOR operations and inter-process
     * communication to efficiently compute tensor contractions that exceed the memory capacity or
     * computational resources of a single GPU. The operation automatically handles data redistribution,
     * local contractions, and result aggregation across the participating processes.
     *
     * The user is responsible for calling \ref cutensorMpDestroyOperationDescriptor to free the
     * resources associated with the descriptor once it is no longer needed.
     *
     * \param[in] handle Opaque handle holding cutensorMp's library context
     * \param[out] desc Pointer to the operation descriptor that will be created and filled with
     *                  information encoding the distributed contraction operation
     * \param[in] descA Distributed tensor descriptor for input tensor A
     * \param[in] modesA Modes of the input tensor A
     * \param[in] opA Unary operator that will be applied to each element of A before it is further processed. The original data of this tensor remains unchanged.
     * \param[in] descB Distributed tensor descriptor for input tensor B
     * \param[in] modesB Modes of the input tensor B
     * \param[in] opB Unary operator that will be applied to each element of B before it is further processed. The original data of this tensor remains unchanged.
     * \param[in] descC Distributed tensor descriptor for input tensor C
     * \param[in] modesC Modes of the input tensor C
     * \param[in] opC Unary operator that will be applied to each element of C before it is further processed. The original data of this tensor remains unchanged.
     * \param[in] descD Distributed tensor descriptor for output tensor D (currently must be identical to descC)
     * \param[in] modesD Modes of the output tensor D
     * \param[in] descCompute Compute descriptor that determines the precision for the operation
     *
     * \retval CUTENSOR_STATUS_SUCCESS The operation completed successfully
     * \retval CUTENSOR_STATUS_NOT_INITIALIZED if the handle is not initialized
     * \retval CUTENSOR_STATUS_INVALID_VALUE if some input data is invalid (this typically indicates a user error)
     * \retval CUTENSOR_STATUS_NOT_SUPPORTED if the combination of tensor configurations is not supported
     * \remarks non-blocking, no reentrant, and thread-safe
     */
    cutensorStatus_t
    cutensorMpCreateContraction(const cutensorMpHandle_t handle, cutensorMpOperationDescriptor_t* desc,
                                const cutensorMpTensorDescriptor_t descA, const int32_t modesA[], cutensorOperator_t opA,
                                const cutensorMpTensorDescriptor_t descB, const int32_t modesB[], cutensorOperator_t opB,
                                const cutensorMpTensorDescriptor_t descC, const int32_t modesC[], cutensorOperator_t opC,
                                const cutensorMpTensorDescriptor_t descD, const int32_t modesD[],
                                const cutensorComputeDescriptor_t descCompute);

    /**
     * \brief Frees all resources related to the provided distributed contraction descriptor.
     *
     * \details This function deallocates all memory and resources associated with a cutensorMp
     * operation descriptor that was previously created by \ref cutensorMpCreateContraction.
     * After calling this function, the descriptor becomes invalid and should not be used in
     * subsequent cutensorMp operations.
     *
     * \param[in,out] desc The cutensorMpOperationDescriptor_t object that will be deallocated
     *
     * \retval CUTENSOR_STATUS_SUCCESS on success and an error code otherwise
     * \remarks blocking, no reentrant, and thread-safe
     */
    cutensorStatus_t cutensorMpDestroyOperationDescriptor(cutensorMpOperationDescriptor_t desc);

    // plan related functions
    /**
     * \brief Creates a plan preference object for controlling distributed tensor operation planning.
     *
     * \details This function creates a preference object that allows users to control various
     * aspects of the execution plan for distributed tensor operations. The preferences include
     * algorithm selection, workspace size limits, and JIT compilation options that affect both
     * the underlying cuTENSOR operations and the distributed communication patterns.
     *
     * The plan preference provides fine-grained control over:
     * - Local cuTENSOR algorithm selection and JIT mode
     * - Distributed algorithm strategy (non-packing, packing with permutation, or packing with P2P)
     * - Workspace size limits for both device and host memory
     * - cuTENSOR workspace preferences
     *
     * The user is responsible for calling \ref cutensorMpDestroyPlanPreference to free the
     * resources associated with the preference object.
     *
     * \param[in] handle Opaque handle holding cutensorMp's library context
     * \param[out] pref Pointer to the plan preference object that will be created
     * \param[in] cutensormp_algo Algorithm selection for distributed communication patterns
     * \param[in] cutensormp_workspace_size_device Maximum device workspace size for cutensorMp operations (bytes), minimum 2GB is required
     * \param[in] cutensormp_workspace_size_host Maximum host workspace size for cutensorMp operations (bytes)
     *
     * \retval CUTENSOR_STATUS_SUCCESS The operation completed successfully
     * \retval CUTENSOR_STATUS_NOT_INITIALIZED if the handle is not initialized
     * \retval CUTENSOR_STATUS_INVALID_VALUE if some input data is invalid (this typically indicates a user error)
     * \remarks non-blocking, no reentrant, and thread-safe
     */
    cutensorStatus_t cutensorMpCreatePlanPreference(const cutensorMpHandle_t handle, cutensorMpPlanPreference_t* pref,
                                                    const cutensorMpAlgo_t cutensormp_algo,
                                                    const uint64_t cutensormp_workspace_size_device,
                                                    const uint64_t cutensormp_workspace_size_host);

    /**
     * \brief Frees all resources related to the provided plan preference object.
     *
     * \details This function deallocates all memory and resources associated with a cutensorMp
     * plan preference object that was previously created by \ref cutensorMpCreatePlanPreference.
     * After calling this function, the preference object becomes invalid and should not be used in
     * subsequent cutensorMp operations.
     *
     * \param[in,out] pref The cutensorMpPlanPreference_t object that will be deallocated
     *
     * \retval CUTENSOR_STATUS_SUCCESS on success and an error code otherwise
     * \remarks blocking, no reentrant, and thread-safe
     */
    cutensorStatus_t cutensorMpDestroyPlanPreference(cutensorMpPlanPreference_t pref);

    /**
     * \brief Creates an execution plan for distributed tensor contractions.
     *
     * \details This function creates an optimized execution plan for the distributed tensor
     * contraction encoded by the operation descriptor. The plan selects the most appropriate
     * algorithms and communication strategies based on the tensor distributions, available
     * resources, and user preferences.
     *
     * The planning process analyzes the distributed tensor layout, communication requirements,
     * and computational resources to determine an efficient execution strategy. This may involve
     * data redistribution, local contractions, and result aggregation phases that minimize
     * communication overhead while maximizing computational efficiency.
     *
     * The user is responsible for calling \ref cutensorMpDestroyPlan to free the
     * resources associated with the plan once it is no longer needed.
     *
     * \param[in] handle Opaque handle holding cutensorMp's library context
     * \param[out] plan Pointer to the execution plan object that will be created
     * \param[in] desc Operation descriptor encoding the distributed contraction
     *                 (created by \ref cutensorMpCreateContraction)
     * \param[in] pref Plan preference object specifying algorithm and workspace preferences
     *                 (may be NULL for default preferences)
     *
     * \retval CUTENSOR_STATUS_SUCCESS The operation completed successfully
     * \retval CUTENSOR_STATUS_NOT_INITIALIZED if the handle is not initialized
     * \retval CUTENSOR_STATUS_INVALID_VALUE if some input data is invalid (this typically indicates a user error)
     * \retval CUTENSOR_STATUS_NOT_SUPPORTED if no viable execution plan could be found
     * \remarks calls asynchronous functions, no reentrant, and thread-safe
     */
    cutensorStatus_t cutensorMpCreatePlan(const cutensorMpHandle_t handle, cutensorMpPlan_t* plan,
                                          const cutensorMpOperationDescriptor_t desc,
                                          const cutensorMpPlanPreference_t pref);

    /**
     * \brief Frees all resources related to the provided distributed contraction plan.
     *
     * \details This function deallocates all memory and resources associated with a cutensorMp
     * execution plan that was previously created by \ref cutensorMpCreatePlan.
     * After calling this function, the plan becomes invalid and should not be used in
     * subsequent cutensorMp operations.
     *
     * \param[in,out] plan The cutensorMpPlan_t object that will be deallocated
     *
     * \retval CUTENSOR_STATUS_SUCCESS on success and an error code otherwise
     * \remarks blocking, no reentrant, and thread-safe
     */
    cutensorStatus_t cutensorMpDestroyPlan(cutensorMpPlan_t plan);

    /**
     * \brief Retrieves information about an already-created plan (see \ref cutensorPlanAttribute_t)
     *
     * \param[in] plan Denotes an already-created plan (e.g., via \ref cutensorMpCreatePlan)
     * \param[in] attr Requested attribute.
     * \param[out] buf On successful exit: Holds the information of the requested attribute.
     * \param[in] sizeInBytes size of `buf` in bytes.
     * \retval CUTENSOR_STATUS_SUCCESS The operation completed successfully.
     * \retval CUTENSOR_STATUS_INVALID_VALUE if some input data is invalid (this typically indicates an user error).
     */
  cutensorStatus_t cutensorMpPlanGetAttribute(const cutensorMpHandle_t handle, const cutensorMpPlan_t plan,
                                              const cutensorMpPlanAttribute_t attribute, void* buf,
                                              const size_t sizeInBytes);

    /**
     * \brief Performs a distributed tensor contraction across multiple processes.
     *
     * \details This function executes the distributed tensor contraction
     * \f$ D = \alpha \mathcal{A} \mathcal{B} + \beta \mathcal{C} \f$
     * according to the execution plan created by \ref cutensorMpCreatePlan. The operation
     * coordinates computation and communication across multiple processes and GPUs to efficiently
     * perform tensor contractions that exceed the capacity of a single device.
     *
     * The execution involves several phases:
     * 1. Data redistribution to align tensor blocks for efficient computation
     * 2. Local tensor contractions using cuTENSOR on each participating device
     * 3. Communication and aggregation of partial results across processes
     * 4. Final result assembly in the distributed output tensor
     *
     * All participating processes in the MPI communicator must call this function with consistent
     * parameters. The input and output tensors must be distributed according to their respective
     * tensor descriptors, with each process providing its local portion of the data.
     *
     * \param[in] handle Opaque handle holding cutensorMp's library context
     * \param[in] plan Execution plan for the distributed contraction
     *                 (created by \ref cutensorMpCreatePlan)
     * \param[in] alpha Scaling factor for the A*B product.
     *                  Pointer to host memory with data type determined by the compute descriptor. The data type follows that of cuTENSOR (i.e., the data type of the scalar is deptermined by the data type of `C`:`CUDA_R_16F` and `CUDA_R_16BF` use `CUDA_R_32F`scalars, all data types of the scalar are identical to the type of `C`)
     * \param[in] A Pointer to the local portion of distributed tensor A in GPU memory
     * \param[in] B Pointer to the local portion of distributed tensor B in GPU memory
     * \param[in] beta Scaling factor for tensor C.
     *                 Pointer to host memory with data type determined by the compute descriptor. The data type follows that of cuTENSOR (i.e., the data type of the scalar is deptermined by the data type of `C`:`CUDA_R_16F` and `CUDA_R_16BF` use `CUDA_R_32F`scalars, all data types of the scalar are identical to the type of `C`)
     * \param[in] C Pointer to the local portion of distributed tensor C in GPU memory
     * \param[out] D Pointer to the local portion of distributed tensor D in GPU memory (may be identical to C)
     * \param[in] device_workspace Pointer to device workspace memory
     *                             (size determined by \ref cutensorMpPlanGetAttribute with
     *                              CUTENSORMP_PLAN_REQUIRED_WORKSPACE_DEVICE)
     * \param[in] host_workspace Pointer to host workspace memory
     *                           (size determined by \ref cutensorMpPlanGetAttribute with
     *                            CUTENSORMP_PLAN_REQUIRED_WORKSPACE_HOST)
     *
     * \retval CUTENSOR_STATUS_SUCCESS The operation completed successfully
     * \retval CUTENSOR_STATUS_NOT_INITIALIZED if the handle is not initialized
     * \retval CUTENSOR_STATUS_INVALID_VALUE if some input data is invalid (this typically indicates a user error)
     * \retval CUTENSOR_STATUS_NOT_SUPPORTED if the operation is not supported with the given configuration
     * \retval CUTENSOR_STATUS_INSUFFICIENT_WORKSPACE if the provided workspace is insufficient
     * \retval CUTENSOR_STATUS_ARCH_MISMATCH if the plan was created for a different device architecture
     * \retval CUTENSOR_STATUS_CUDA_ERROR if a CUDA error occurred during execution
     * \remarks calls asynchronous functions, no reentrant, and thread-safe
     */
    cutensorStatus_t cutensorMpContract(const cutensorMpHandle_t handle, const cutensorMpPlan_t plan, const void* alpha,
                                        const void* A, const void* B, const void* beta, const void* C, void* D,
                                        void* device_workspace, void* host_workspace);

#ifdef __cplusplus
}
#endif
